import sys


def main():
    try:
        from trawpaw import Trawpaw
        from trawpaw.doc import VERSION, DOCUMENT
        from argparse import ArgumentParser, RawTextHelpFormatter, Namespace
        from prompt_toolkit import prompt
        from prompt_toolkit.history import FileHistory
        import colorama
        import pydoc
        import warnings

        colorama.init(convert=True)
        Fore = colorama.Fore

        parser = ArgumentParser(
            usage="trawpaw [options] <file>",
            description="Trawpaw v" + VERSION,
            formatter_class=RawTextHelpFormatter,
        )
        running_method = parser.add_mutually_exclusive_group(required=False)
        parser.add_argument(
            "--usage",
            "-u",
            action="store_true",
            help="Show usage information and quit.",
        )
        parser.add_argument(
            "file",
            nargs="?",
            help="Path to the Trawpaw source code file or file to listen",
        )
        parser.add_argument(
            "--cells",
            "-m",
            type=int,
            default=128,
            help="Number of memory cells to use (1 <= cells <= 65536) (default: 128).",
        )
        parser.add_argument(
            "--maxvaluepercell",
            "-v",
            type=int,
            default=127,
            help="Maximum value per cell (0 <= maxvaluepercell <= 65535) (default: 127).",
        )
        parser.add_argument(
            "--version",
            "-V",
            action="version",
            version=VERSION,
            help="Show version information and quit.",
        )
        parser.add_argument(
            "--trawpawl",
            "-tpwl",
            type=str,
            metavar="OUT_FILE",
            required=False,
            help="Enable trawpawl and set the file to output",
        )
        running_method.add_argument(
            "--waste_preview", action="store_true", help="Run waste (preview) code"
        )
        running_method.add_argument(
            "--waste", action="store_true", help="Run waste code"
        )
        running_method.add_argument(
            "--brainfuck", "-bf", action="store_true", help="Run Brainfuck code"
        )
        running_method.add_argument(
            "--nohistories",
            "-nh",
            action="store_true",
            help="Tell REPL do not use histories",
        )
        parser.add_argument(
            "--charset",
            "-c",
            type=str,
            default="utf-8",
            help="Assign charset to read file.",
        )
        parser.add_argument("--silent", "-s", action="store_true", help="silent mode")

        args: Namespace = parser.parse_args()
        trawpaw_executor: Trawpaw
        try:
            trawpaw_executor = Trawpaw(args.cells, args.maxvaluepercell)
        except AssertionError as e:
            print(f"ERR: {e}")
            sys.exit(1)

        if args.usage:
            pydoc.pager(DOCUMENT)  # type: ignore
            sys.exit(0)
        elif args.trawpawl:
            if (args.waste or args.waste_preview) and (not args.silent):
                warnings.warn(
                    "Ignoring --waste or --waste_preview because enabled --trawpawl"
                )
            if not args.file:
                parser.error("Filepath is required when enabled --trawpawl")
            else:
                import os
                import time
                from trawpaw.tools import compileTrawpawl
                from math import floor

                print(f"Listening {args.file}")

                def watch_file_content(file_path, interval=1):
                    if not os.path.exists(file_path):
                        print(f"File not exists: {file_path}")
                        return

                    try:
                        with open(file_path, "rb", encoding=args.charset) as f:
                            last_content = f.read()

                            while True:
                                with open(file_path, "r", encoding=args.charset) as f:
                                    current_content = f.read()

                                if current_content != last_content:
                                    print("File changed, compiling...")
                                    start_time = time.time()

                                    result = compileTrawpawl(
                                        current_content,
                                        cells=args.cells,
                                        maxvaluepercell=args.maxvaluepercell,
                                        silent=args.silent,
                                    )

                                    with open(
                                        args.trawpawl, "w", encoding=args.charset
                                    ) as f:
                                        f.write(result)
                                        print(
                                            f"Ok. Took {floor((time.time() - start_time) * 100000) / 100}ms"
                                        )
                                    last_content = current_content

                                time.sleep(interval)
                    except FileNotFoundError:
                        print("Cannot parse this file.")
                        sys.exit(1)
                    except LookupError:
                        print("Unknown charset.")
                        sys.exit(1)
                    except PermissionError:
                        print(
                            "No permission to read or write file. You may forgot to chmod it."
                        )
                        sys.exit(1)
                    except KeyboardInterrupt:
                        sys.exit(0)

                watch_file_content(args.file)

        elif args.file:
            try:
                with open(args.file, "r", encoding=args.charset) as f:
                    code: str = f.read()
                    if args.waste_preview:
                        trawpaw_executor.datalist["a"] = {"type": "number", "value": 0}
                        trawpaw_result = trawpaw_executor.runWastePreview(code, "a")
                    elif args.waste:
                        trawpaw_executor.datalist["a"] = {"type": "number", "value": 0}
                        trawpaw_result = trawpaw_executor.runWaste(code, "a")
                    elif args.brainfuck:
                        trawpaw_result = trawpaw_executor.runBrainfk(code)
                    else:
                        trawpaw_result = trawpaw_executor.execute(code)
                    print(end="\n")
                    if trawpaw_result.status == 1:
                        print(Fore.RED + trawpaw_result.message + Fore.RESET)
                    f.close()
                sys.exit(0)
            except FileNotFoundError:
                print("Cannot parse this file.")
                sys.exit(1)
            except LookupError:
                print("Unknown charset.")
                sys.exit(1)
            except PermissionError:
                print("No permission to read file. You may forgot to chmod it.")
                sys.exit(1)
        else:
            if args.nohistories:
                histories = None
            else:
                histories = FileHistory(".tphistories")

            if args.waste:
                print(
                    "View https://github.com/ChenQingMua/WasteLanguage-Professional for more information"
                    + "\nDownload the genuine WasteLanguage, not only `trawpaw --waste`!!!"
                )
            elif args.waste_preview:
                print(
                    "View https://github.com/ChenQingMua/WasteLanguage-Preview for more information"
                    + "\nDownload the genuine WasteLanguage, not only `trawpaw --waste_preview`!!!"
                )
            else:
                print("Run `trawpaw --usage` for more information")

            if sys.platform == "darwin":
                print("Press Cmd+C or Cmd+D to exit.")
            else:
                print("Press Ctrl+C or Ctrl+D to exit.")

            if args.waste or args.waste_preview:
                trawpaw_executor.datalist["a"] = {"type": "number", "value": 0}
                if args.waste:
                    code = prompt("[waste c:0] ", history=histories)
                else:
                    code = prompt("[waste] ", history=histories)
            elif args.brainfuck:
                code = prompt("[bf c:0] ", history=histories)
            else:
                code = prompt("[c:0 v:0] ", history=histories)
            while True:
                if args.waste_preview:
                    trawpaw_result = trawpaw_executor.runWastePreview(
                        code, "a", silentMode=args.silent
                    )
                elif args.waste:
                    trawpaw_result = trawpaw_executor.runWaste(
                        code, "a", silentMode=args.silent
                    )
                elif args.brainfuck:
                    trawpaw_result = trawpaw_executor.runBrainfk(
                        code, silentMode=args.silent
                    )
                else:
                    trawpaw_result = trawpaw_executor.execute(
                        code, silentMode=args.silent
                    )
                print(end="\n")
                if trawpaw_result.status == 1:
                    print(trawpaw_result.message)
                if args.waste:
                    code = prompt(
                        f"[waste c:{trawpaw_result.cursor}] ", history=histories
                    )
                elif args.waste_preview:
                    code = prompt("[waste] ", history=histories)
                elif args.brainfuck:
                    code = prompt(f"[bf c:{trawpaw_result.cursor}] ", history=histories)
                else:
                    code = prompt(
                        f"[c:{trawpaw_result.cursor} v:{trawpaw_result.datalistlength}] ",
                        history=histories,
                    )
    except KeyboardInterrupt:
        sys.exit(0)
    except EOFError:
        sys.exit(0)


if __name__ == "__main__":
    main()
else:
    raise ImportError("This is REPL, not a module")
