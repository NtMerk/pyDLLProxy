import pefile
import argparse
import os
import shutil

dll_directives = []

def build_template():
    full_str = "#include <Windows.h>\n\n"
    full_str += '\n'.join(dll_directives)
    full_str += """\n
BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,
    DWORD fdwReason,
    LPVOID lpvReserved)
{
    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        // Your code goes here
        break;

    case DLL_THREAD_ATTACH:
        break;

    case DLL_THREAD_DETACH:
        break;

    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
"""
    return full_str

def parse_arguments():
    parser = argparse.ArgumentParser(description='pyDLLProxy will generate the necessary C/C++ directives in order to aid in the development of DLL Proxying techniques.')
    parser.add_argument('dll_path', type=str, help='Full path to the DLL to Proxy.')
    parser.add_argument('dll_new_name', type=str, help='New name for the DLL to proxy to.')

    parser.add_argument('-O', '--output', type=str, help='Output file for the exports.')
    parser.add_argument('-T', '--template', type=str, choices=['c', 'cpp'], default='c', help='Generate a DLL template with the exports.')

    return parser.parse_args()

def convert_to_directive(dll_export, dll_path, dll_new_name):
    if dll_new_name.lower().endswith(".dll"):
        dll_new_name = os.path.splitext(dll_new_name)[0]
    return "#pragma comment(linker, \"/export:\\\"" + dll_export + "=" + os.path.dirname(dll_path).replace("\\", "/") + "/" + dll_new_name + "." + dll_export + "\\\"\")"

def parse_dll(dll_path, new_name):
    pe = pefile.PE(dll_path)
    print("[+] Parsing DLL at", dll_path)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]])
    print("[+] Found", len(pe.DIRECTORY_ENTRY_EXPORT.symbols), "exports.")
    
    for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        dll_directives.append(convert_to_directive(export.name.decode(), dll_path, new_name))

def main():
    args = parse_arguments()

    try:
        parse_dll(args.dll_path, args.dll_new_name)
        if args.output:
            output = args.output
            print("[+] Creating folder", output)
            os.makedirs(output)
            print("[+] Creating template files")
            chosen_template = args.template
            with open(os.path.abspath(output) + "/" + output + chosen_template, 'w') as f: f.write(build_template())
            new_name = args.dll_new_name
            if new_name.lower().endswith(".dll"):
                new_name = os.path.splitext(args.dll_new_name)[0]
            shutil.copy(args.dll_path, os.path.abspath(output) + "/" + new_name + ".dll")
        else:
            print(*dll_directives, sep='\n')

    except Exception as e:
        print("[-] An exception has ocurred:", e)

if __name__ == "__main__":
    main()