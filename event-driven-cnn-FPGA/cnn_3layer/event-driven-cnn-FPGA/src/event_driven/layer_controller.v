// ============================================================
// layer_controller.v
// 3-layer CNN controller (event-driven)
// ============================================================

module layer_controller (
    input  wire clk,
    input  wire rst_n,

    input  wire start,
    input  wire event_queue_empty,
    input  wire pe_idle,

    output reg  layer_active,
    output reg  [1:0] layer_id,   // 0,1,2
    output reg  done
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            layer_id     <= 2'd0;
            layer_active <= 1'b0;
            done         <= 1'b0;
        end else begin
            if (start) begin
                layer_active <= 1'b1;
                done <= 1'b0;
                layer_id <= 2'd0;
            end

            if (layer_active && event_queue_empty && pe_idle) begin
                if (layer_id == 2'd2) begin
                    layer_active <= 1'b0;
                    done <= 1'b1;
                end else begin
                    layer_id <= layer_id + 1'b1;
                end
            end
        end
    end

endmodule
