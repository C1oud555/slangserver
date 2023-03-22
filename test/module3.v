module module3 #(
    parameter DW = 8
) (
    input [DW-1:0] data_in1,
    input [DW-1:0] data_in2,
    input [DW-1:0] data_in3,

    output [DW-1:0] out1,
    output [DW-1:0] out2
);

  assign out1 = data_in1 + data_in2;
  assign out2 = data_in2 + data_in3

endmodule

interface interface1;
  logic [255:0] port1;
endinterface  //interface1
