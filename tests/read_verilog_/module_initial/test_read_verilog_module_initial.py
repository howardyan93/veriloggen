import read_verilog_module_initial

expected_verilog = """
module test #
  ( 
   parameter WIDTH = 8
  )
  (
  );

  reg CLK;
  reg RST;
  wire [(WIDTH-1)+1-1:0] LED;

  blinkled #
   (
    .WIDTH(WIDTH)
   )
  uut
   (
    .CLK(CLK),
    .RST(RST),
    .LED(LED)
   );

  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end

  initial begin
    RST = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #1000;
    $finish;
  end

endmodule


module blinkled #
  (
   parameter WIDTH = 8
  )
  (
   input CLK, 
   input RST, 
   output reg [((WIDTH-1)+1)-1:0] LED
  );
  reg [((32-1)+1)-1:0] count;
  always @(posedge CLK) begin
    if(RST) begin        
      count <= 0;
    end else begin
      if(count == 1023) begin
        count <= 0;
      end else begin
        count <= count + 1;
      end
    end 
  end 
  always @(posedge CLK) begin
    if(RST) begin        
      LED <= 0;
    end else begin
      if(count == 1023) begin        
        LED <= LED + 1;
      end  
    end 
  end 
endmodule
"""

def test():
    test_module, test_bench = read_verilog_module_initial.mkLedTest()
    code = ''.join([ test_bench.to_verilog(), test_module.to_verilog() ])
    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
