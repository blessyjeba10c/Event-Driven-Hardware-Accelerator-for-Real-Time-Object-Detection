
module event_queue #(
    parameter DATA_WIDTH = 64,
    parameter DEPTH = 32
)(
    input  wire clk,
    input  wire rst_n,

    // Push from CSC
    input  wire in_valid,
    input  wire [DATA_WIDTH-1:0] in_data,
    output wire in_ready,

    // Pop to router / PE
    output wire out_valid,
    output wire [DATA_WIDTH-1:0] out_data,
    input  wire out_ready,

    output wire empty
);

    reg [DATA_WIDTH-1:0] mem [0:DEPTH-1];
    reg [$clog2(DEPTH):0] wptr, rptr, count;

    assign in_ready  = (count < DEPTH);
    assign out_valid = (count > 0);
    assign out_data  = mem[rptr];
    assign empty     = (count == 0);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wptr  <= 0;
            rptr  <= 0;
            count <= 0;
        end else begin
            // Push event
            if (in_valid && in_ready) begin
                mem[wptr] <= in_data;
                wptr <= wptr + 1'b1;
                count <= count + 1'b1;
            end

            // Pop event
            if (out_valid && out_ready) begin
                rptr <= rptr + 1'b1;
                count <= count - 1'b1;
            end
        end
    end

endmodule
