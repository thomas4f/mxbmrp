# memory_reader.py

import ctypes
from ctypes import wintypes
from typing import Optional

import psutil

PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

OpenProcess = ctypes.windll.kernel32.OpenProcess
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
CloseHandle = ctypes.windll.kernel32.CloseHandle


def get_pid(proc_name, verbose):
    # Retrieve the PID of the specified process by its name.
    for process in psutil.process_iter(["pid", "name"]):
        if process.info["name"].lower() == proc_name.lower():
            if verbose:
                print(f"PID: {process.info['pid']}")
            return process.info["pid"]
    return None


def get_base_addr(proc_pid, proc_name, verbose):
    # Obtain the base memory address of the specified module within the given process.
    proc = psutil.Process(proc_pid)
    for memory_map in proc.memory_maps(grouped=False):
        if memory_map.path.lower().endswith(proc_name.lower()):
            addr_start = memory_map.addr.split("-")[0]
            base_addr = int(addr_start, 16)
            if verbose:
                print(f"Base address: 0x{base_addr:X}")
            return base_addr


def open_proc(proc_pid, verbose):
    # Open a handle to the process with read and query permissions.
    access = PROCESS_VM_READ | PROCESS_QUERY_INFORMATION
    proc_handle = OpenProcess(access, False, proc_pid)
    if verbose:
        print(f"Process handle: {proc_handle}")
    return proc_handle


def pid_exists(proc_pid):
    if psutil.pid_exists(proc_pid):
        return True


def read_mem(proc_pid, proc_handle, addr_name, addr_loc, num_bytes, verbose):
    # Read a specified number of bytes from a given memory address within the process.
    if verbose:
        print(f"Reading {addr_name} from 0x{addr_loc:X} ({num_bytes} bytes)")

    buffer = ctypes.create_string_buffer(num_bytes)
    bytes_read = ctypes.c_size_t()
    if ReadProcessMemory(
        proc_handle,
        ctypes.c_void_p(addr_loc),
        buffer,
        num_bytes,
        ctypes.byref(bytes_read),
    ):
        raw_data = buffer.raw[: bytes_read.value]

        # Conditionally truncate at the first null byte, except for 'server_ip'.
        if addr_name != "server_ip":
            null_index = raw_data.find(b"\x00")
            if null_index != -1:
                raw_data = raw_data[:null_index]

        if verbose:
            print(f"Raw value: {raw_data}")
        return raw_data
    return None


def search_mem(
    proc_pid, proc_handle, addr_name, search_bytes: bytes, verbose
) -> Optional[int]:
    # Search memory for specified value and return address.
    if verbose:
        print(f"Searching for {addr_name} by {search_bytes} ...")

    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BaseAddress", ctypes.c_void_p),
            ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", wintypes.DWORD),
            ("RegionSize", ctypes.c_size_t),
            ("State", wintypes.DWORD),
            ("Protect", wintypes.DWORD),
            ("Type", wintypes.DWORD),
        ]

    MEM_COMMIT = 0x1000
    PAGE_READONLY = 0x02
    PAGE_READWRITE = 0x04
    PAGE_EXECUTE_READ = 0x20
    PAGE_EXECUTE_READWRITE = 0x40
    PAGE_GUARD = 0x100

    PAGE_READABLE = {
        PAGE_READONLY,
        PAGE_READWRITE,
        PAGE_EXECUTE_READ,
        PAGE_EXECUTE_READWRITE,
    }

    VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
    VirtualQueryEx.restype = ctypes.c_size_t
    VirtualQueryEx.argtypes = [
        wintypes.HANDLE,
        wintypes.LPCVOID,
        ctypes.POINTER(MEMORY_BASIC_INFORMATION),
        ctypes.c_size_t,
    ]

    address = 0x0
    max_address = 0x7FFFFFFFFFFFFFFF

    mbi = MEMORY_BASIC_INFORMATION()
    found_address = None

    while address < max_address:
        bytes_returned = VirtualQueryEx(
            proc_handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi)
        )
        if not bytes_returned:
            break

        if (
            mbi.State == MEM_COMMIT
            and (mbi.Protect & 0xFF) in PAGE_READABLE
            and not (mbi.Protect & PAGE_GUARD)
        ):

            region_size = mbi.RegionSize
            buffer = ctypes.create_string_buffer(region_size)
            bytes_read = ctypes.c_size_t()

            if ReadProcessMemory(
                proc_handle,
                ctypes.c_void_p(address),
                buffer,
                region_size,
                ctypes.byref(bytes_read),
            ):
                chunk = buffer.raw[: bytes_read.value]
                idx = chunk.find(search_bytes)
                if idx != -1:
                    found_address = address + idx
                    if verbose:
                        print(f"Found {addr_name} at address: 0x{found_address:X}")
                    return found_address

        address += mbi.RegionSize

    if not found_address:
        print(f"No occurrences of {addr_name} found")
        return None


def decode_data(raw_data, addr_name):
    # Decode raw memory data based on type.
    if addr_name in [
        "bike_name",
        "local_server_name",
        "local_server_password",
        "track_name",
        "server_password",
        "server_name",
    ]:
        decoded_data = raw_data.decode("ascii").rstrip("\x00")

    if addr_name == "server_ip":
        decoded_data = ".".join(str(b) for b in raw_data[:4])

    if addr_name == "server_port":
        decoded_data = int.from_bytes(raw_data[:2], byteorder="big")

    return decoded_data


def close_handle(proc_pid, proc_handle, verbose):
    # Close the previously opened process handle.
    if proc_handle and verbose:
        print(f"Closing handle {proc_handle} to PID {proc_pid}")
        CloseHandle(proc_handle)


def attach_to_process(proc_name, update_interval, verbose):
    # Attach to the target process by retrieving its PID, base address, and opening a handle.
    if verbose:
        print(f"Trying to attach to {proc_name}")
    proc_pid = get_pid(proc_name, verbose)
    if not proc_pid:
        print(
            f"Process {proc_name} not found, retrying in {update_interval} seconds ..."
        )
        return False

    base_addr = get_base_addr(proc_pid, proc_name, verbose)
    if not base_addr:
        print(f"Unable to determine base address of {proc_name}")
        return False

    proc_handle = open_proc(proc_pid, verbose)
    if not proc_handle:
        print(f"Failed to create handle for PID {proc_pid}")
        return False

    print(f"Attached to {proc_name} (PID: {proc_pid}) with handle {proc_handle}")
    return proc_pid, base_addr, proc_handle
