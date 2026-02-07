module event_router (
    input clk,
    input rst_n,
    input in_valid,
    input [63:0] in_data,
    output in_ready,
    output reg out_valid,
    output reg [63:0] out_data,
    input out_ready
);
assign in_ready = out_ready || !out_valid;

always @(posedge clk) begin
    if (!rst_n) out_valid <= 0;
    else if (in_valid && in_ready) begin
        out_valid <= 1;
        out_data <= in_data;
    end else if (out_valid && out_ready)
        out_valid <= 0;
end
endmodule
