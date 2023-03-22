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

import logging

logger = logging.getLogger("slangserver logger")

svserver = LanguageServer("slangserver", "v0.1")


def _publish_diagnostics(server: LanguageServer, uri: str) -> None:
    logger.warn(f"_publish_diagnostics of {uri}")
    if uri not in server.workspace.documents:
        return

    root_path = server.workspace.root_path
    doc = server.workspace.get_document(uri)
    diagnostics = slang_util.diagnose(root_path, uri)
    logger.warn(f"And the diagnose result is {diagnostics}")
    server.publish_diagnostics(uri, diagnostics)


@svserver.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams):
    items = []
    document = svserver.workspace.get_document(params.text_document.uri)
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


@svserver.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save_diagnose(params: DidSaveTextDocumentParams) -> None:
    _publish_diagnostics(svserver, params.text_document.uri)
