
module PE_event (
    input  wire clk,
    input  wire rst_n,

    input  wire evt_valid,
    input  wire [63:0] evt_data,
    output wire evt_ready,

    output reg  psum_valid,
    output reg  [31:0] psum,
    output reg  [15:0] psum_idx,

    input  wire psum_ready
);

    reg busy;
    reg [15:0] act;
    reg [15:0] weight;
    reg [15:0] idx;

    assign evt_ready = !busy;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            busy       <= 1'b0;
            psum_valid <= 1'b0;
        end else begin
            // Accept event
            if (evt_valid && evt_ready) begin
                act    <= evt_data[63:48];
                weight <= evt_data[47:32];
                idx    <= evt_data[15:0];
                busy   <= 1'b1;
            end

            // Compute MAC
            if (busy) begin
                psum     <= act * weight;
                psum_idx <= idx;
                psum_valid <= 1'b1;
                busy <= 1'b0;
            end

            // Handshake complete
            if (psum_valid && psum_ready) begin
                psum_valid <= 1'b0;
            end
        end
    end

endmodule
