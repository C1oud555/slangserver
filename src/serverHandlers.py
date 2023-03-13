from pyslang import (
    SourceManager,
    CompilationOptions,
    Bag,
    SourceBuffer,
    Compilation,
    SyntaxTree,
    DiagnosticEngine,
    TextDiagnosticClient,
    Diagnostic,
    ReportedDiagnostic,
)
from dataclasses import dataclass, field
from pathlib import Path
import logging

logger = logging.getLogger("svlangserver logger")


@dataclass
class DiagnosticReport:
    file_name: str
    message: str
    severity: str
    line: int
    col: int


class ServerHandler:
    def __init__(self, root_path: str, options: str) -> None:
        self.sources = ProjectSources()
        self.sources.set_root_path(root_path)
        self.bag = Bag()
        self.coptions = CompilationOptions()

    def addAllFiles(self):
        logger.warn("add files")
        self.sources.addAllFiles()

    def updateDiagnostics(self) -> list[DiagnosticReport]:
        # recompile the design
        compilation = self.sources.compile()
        sm = self.sources.get_source_manager()

        engine = DiagnosticEngine(sm)
        # rewrite engine
        client = TextDiagnosticClient()
        engine.addClient(client)

        client.clear()

        diags = compilation.getAllDiagnostics()
        res = []
        for diag in diags:
            engine.issue(diag)
            sm = self.sources.get_source_manager()
            rel_filename = sm.getFileName(diag.location)
            file_name = Path(rel_filename).absolute()

            message = engine.formatMessage(diag)
            line = sm.getLineNumber(diag.location)
            col = sm.getColumnNumber(diag.location)
            severity = engine.getSeverity(diag.code, diag.location)

            res.append(
                DiagnosticReport(
                    file_name,
                    message,
                    severity,
                    line,
                    col,
                )
            )
        logger.warn(f"actual result {client.getString()}")
        return res


class ProjectSources:
    def __init__(self) -> None:
        self.__config = init_config()
        self.__config.loaded = False
        self.__dirty = False
        self.__sm = SourceManager()
        self.__files_map: dict[Path, file_info] = {}
        self.__loaded_buffers: dict[Path, SourceBuffer] = {}
        # mutex ???

    def addAllFiles(self):
        sm = self.__sm
        extensions = ["sv", "v", "vh", "svh"]
        for ext in extensions:
            for file in Path(self.__config.rootPath).rglob(f"*.{ext}"):
                self.addFile(file, True)
                logger.warn(f" Add file {file}")

    def set_root_path(self, path: Path) -> None:
        self.__config.rootPath = path.absolute()
        # locate_init_config(self.__config.rootPath)

    def addFile(self, path: Path, userLoaded: bool) -> None:
        # TODO: auto loaded something
        res = self.__files_map.get(path)
        if not res:
            info = file_info("", False, userLoaded)
            self.__files_map[path] = info

        self.__dirty |= userLoaded

    def get_source_manager(self) -> SourceManager:
        return self.__sm

    def compile(self) -> Compilation:
        coptions = CompilationOptions()
        coptions.lintMode = False
        # options = Bag()
        # options.set(coptions)

        compilation = Compilation()
        print("Re-compiling sources")

        self.__loaded_buffers.clear()
        self.__sm = SourceManager()
        for dpath in self.__config.include_directories:
            self.__sm.addUserDirectory(dpath.absolute())

        for filepath, info in self.__files_map.items():
            buff = SourceBuffer
            if info.modified:
                buff = self.__sm.assignText(filepath, info.content)
            else:
                buff = self.__sm.readSource(filepath)
            tree = SyntaxTree.fromBuffer(buff, self.__sm)
            if not info.userLoaded:
                tree.isLibrary = True
            compilation.addSyntaxTree(tree)

        return compilation


@dataclass
class init_config:
    loaded: bool = False
    rootPath: Path = Path(".")
    library_directories: set[Path] = field(default_factory=set)
    include_directories: set[Path] = field(default_factory=set)


@dataclass
class file_info:
    content: str
    modified: bool
    userLoaded: bool


def main():
    # handler = ServerHandler("", "")
    # handler.sources.addFile("test/module1.sv", True)
    # handler.sources.addFile("test/module2.sv", True)
    # handler.sources.addFile("test/module3.sv", True)
    # handler.updateDiagnostics()
    path = Path(".")
    extensions = ["sv", "v", "vh", "svh"]
    for ext in extensions:
        for file in path.rglob(f"*.{ext}"):
            print(file)


if __name__ == "__main__":
    main()
