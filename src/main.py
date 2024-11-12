# main.py

import time

from file_reader import load_config, load_shader_tpl
from memory_reader import (
    attach_to_process,
    close_handle,
    decode_data,
    pid_exists,
    read_mem,
    search_mem,
)
from shader_generator import format_content, gen_shader
from pathlib import Path
import sys


def main():
    print("Starting memory_reader_project for MX Bikes beta19b")
    print("Press CTRL + C to to exit\n")

    # Read files
    config = load_config("config.yaml")
    shader_src_path = load_shader_tpl(config["shader_src_path"])

    # Initialize config variables
    content_tpl = config["content_tpl"]
    shader_dest_path = Path(config["shader_dest_path"]).resolve()
    layer_src_path = Path(config["layer_src_path"]).resolve()
    max_len = config["max_len"]
    update_interval = config["update_interval"]
    verbose = config["verbose"]
    proc_name = config["proc_name"]
    mem_addrs = config["mem_addrs"]
    server_name_offset = config["server_name"]["offset"]
    server_name_data_size = config["server_name"]["data_size"]

    # Initialize other variables
    proc_pid = proc_handle = None
    last_content = None

    try:
        while True:
            # Initialize mem_info object
            mem_info = {
                "bike_name": None,
                "local_server_name": None,
                "local_server_password": None,
                "track_name": None,
                "server_ip": None,
                "server_port": None,
                "server_password": None,
                "server_name": None,
            }

            start_time = time.perf_counter()
            search_str = b""

            # Attach to the target process
            if proc_pid is None or not pid_exists(proc_pid) or proc_handle is None:
                try:
                    proc_pid,base_addr, proc_handle = attach_to_process(proc_name, update_interval, verbose)
                except Exception:
                    if proc_handle is not None:
                        close_handle(proc_pid, proc_handle, verbose)
                        proc_pid = proc_handle = None
                    time.sleep(update_interval)
                    continue
            elif verbose:
                print(f"Already attached to PID {proc_pid} with handle {proc_handle}")

            # Read memory from the target offsets
            for addr_name, addr_info in mem_addrs.items():
                addr_offset = addr_info["addr_offset"]
                data_size = addr_info["data_size"]

                # Calculate address
                addr_loc = base_addr + addr_offset

                # Search data
                raw_data = read_mem(proc_pid, proc_handle, addr_name, addr_loc, data_size, verbose)

                # Decode data
                if raw_data is not None:
                    decoded_data = decode_data(raw_data, addr_name)

                    if verbose:
                        print(f"{addr_name}: {decoded_data}")

                    # Add data to mem_info
                    mem_info[addr_name] = decoded_data

                # Prepare string for mem_search
                if addr_name in ("server_ip", "server_port") and decoded_data:
                    search_str += raw_data

            # Connected to server - search memory for name by ip:port
            if mem_info["server_ip"]:
                addr_loc = search_mem(proc_pid, proc_handle, "server_name", search_str, verbose)
                
                raw_data = read_mem(
                    proc_pid,
                    proc_handle,
                    "server_name",
                    addr_loc + server_name_offset,
                    server_name_data_size,
                    verbose,
                )
                if raw_data is not None:
                    decoded_data = decode_data(raw_data, "server_name")

                    if verbose:
                        print(f"server_name: {decoded_data}")

                    mem_info["server_name"] = decoded_data
            elif verbose:
                print("Not connected to server, skipping server_name search")

            # Format content
            formatted_content = format_content(content_tpl, mem_info, max_len, verbose)

            # Check for changes
            if formatted_content != last_content:
                # Output to console
                for line in formatted_content.splitlines():
                    if ":" in line:
                        key, val = line.split(":", 1)
                        print(f"{key.strip()}: {val.strip()}")

                # Generate shader
                gen_shader(
                    shader_src_path, shader_dest_path, formatted_content, layer_src_path, verbose
                )
                last_content = formatted_content
                print("Shader updated")
            else:
                if verbose:
                    print("Content unchanged, skipping shader update")

            # Display execution time
            if verbose:
                end_time = time.perf_counter()
                elapsed = end_time - start_time
                print(f"Execution time: {elapsed:.4f} seconds")

            # Wait for next read
            if verbose:
                print(f"Sleeping for {update_interval} seconds ...\n")
            time.sleep(update_interval)
    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting")
    finally:
        # Close handle
        if proc_handle is not None:
            close_handle(proc_pid, proc_handle, verbose)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        if hasattr(sys, '_MEIPASS'):
            input("Press Enter to exit...")
