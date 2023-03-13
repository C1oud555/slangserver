from pyslang import SyntaxTree, Compilation, DiagnosticEngine, TextDiagnosticClient, Bag

from lsprotocol.types import Diagnostic, Position, DiagnosticSeverity, Range, Diagnostic

from typing import Optional

from serverHandlers import ServerHandler
from pathlib import Path
import logging

logger = logging.getLogger("svlangserver logger")


def diagnose(root_path: str) -> Optional[Diagnostic]:
    handler = ServerHandler(Path(root_path), "")
    handler.addAllFiles()
    diagnostics = handler.updateDiagnostics()
    res = list()
    for diag in diagnostics:
        logger.warn(type(diag))
        line = diag.line
        col = diag.col
        logger.warn(type(line))
        res.append(
            Diagnostic(
                range=Range(
                    start=Position(line=(line - 1), character=(col - 1)),
                    end=Position(line=line, character=col),
                ),
                message=diag.message,
                severity=DiagnosticSeverity.Error,
                source="compile",
            )
        )

    return res


test_sv1 = """
module memory(
    address,
    data_in,
    data_out,
    read_write,
    chip_en
  );

  input wire [7:0] address, data_in;
  output reg [7:0] data_out;
  input wire read_write, chip_en;

  reg [7:0] mem [0:255];

  always @ (address or data_in or read_write or chip_en)
    if (read_write == 1 && chip_en == 1) begin
      mem[address] = data_in;
  end

  always @ (read_write or chip_en or address)
    if (read_write == 0 && chip_en)
      data_out = mem[address];
    else
      data_out = 0;

  tttt u1(.a(tess))

;
endmodule
"""

test_sv2 = """
module tttt(
input [7: 0] a,
output b
);

assign b = a[1];

function tes;

endfunction

endmodule
"""

# SourceManager
# SourceBuffer
# SourceLocation
# SourceRange
#
# Diagnostics
# DiagnosticEngine
# (TEXT)DiagnosticClient
#
# SyntaxTree
# SyntaxNode
#

sourceManager = SyntaxTree.getDefaultSourceManager()

diag_engine = DiagnosticEngine(sourceManager)
diag_client = TextDiagnosticClient()
diag_engine.addClient(diag_client)

tree1 = SyntaxTree.fromText(test_sv1)
tree2 = SyntaxTree.fromText(test_sv2)

# get diagnostics while parsing
diags1 = tree1.diagnostics

root = tree2.root
print("header:", root.header)
print(root.kind)
for index, member in enumerate(root.members):
    print(f"member: {index}   {member}\nkind: {member.kind}")
body = root.members
print(body)
# print(body.sourceRange.start)
# print(body.sourceRange.start.buffer)
# print(body.sourceRange.end)
print(body.getFirstToken())
print(dir(body))
print("blockname:", root.blockName)

print(root.parent)

for diag in diags1:
    diag_engine.issue(diag)


comp = Compilation()
comp.addSyntaxTree(tree1)
comp.addSyntaxTree(tree2)

# get diagnostics while compilation
diags = comp.getAllDiagnostics()

for diag in diags:
    diag_engine.issue(diag)

print(diag_client.getString())
