import logging

import slang_util
from pygls.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_SAVE,
    CompletionItem,
    CompletionList,
    CompletionParams,
    DidSaveTextDocumentParams,
)

logging.basicConfig(filename="pygls.log", filemode="w", level=logging.INFO)
logger = logging.getLogger("svlangserver logger")

server = LanguageServer("svlangserver", "v0.1")


def _publish_diagnostics(server: LanguageServer, uri: str) -> None:
    if uri not in server.workspace.documents:
        return

    doc = server.workspace.get_document(uri)
    diagnostic = slang_util.diagnose(uri, doc.source)
    diagnostics = [diagnostic] if diagnostic else []
    server.publish_diagnostics(uri, diagnostics)


@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams):
    items = []
    document = server.workspace.get_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    logger.info("get completions request")
    if current_line.endswith("hello."):
        logger.info("get completions with hello.")
        items = [
            CompletionItem(label="world"),
            CompletionItem(label="world1"),
            CompletionItem(label="world2"),
            CompletionItem(label="world3"),
            CompletionItem(label="world4"),
            CompletionItem(label="firend"),
        ]
    return CompletionList(is_incomplete=False, items=items)


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save_diagnose(params: DidSaveTextDocumentParams) -> None:
    _publish_diagnostics(server, params.text_document.uri)
