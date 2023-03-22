module module2 #(
    parameter DW = 8
) (
    input [DW-1:0] data_in1,
    input [DW-1:0] data_in2,
    input [DW-1:0] data_in3,

    output [DW-1:0] out1,
    output [DW-1:0] out2
);


  module3 u3 (
      .data_in1(data_in1),
      .data_in2(data_in2),
      /* .data_in3(data_in3), */

      .out1(out1),
      .out2(out2)
  );


endmodule
