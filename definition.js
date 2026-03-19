const TCS34725ColorBlock = "#ae00ae";

// ============================================================
// OLD BLOCKS (unchanged)
// ============================================================

Blockly.Blocks["uno_tcs34725_read"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      tooltip: "",
      message0: "cảm biến màu sắc đọc giá trị %1",
      args0: [
        {
          type: "field_dropdown",
          name: "RGB",
          options: [
            ["RED", "r"],
            ["GREEN", "g"],
            ["BLUE", "b"],
          ],
        }
      ],
      output: "Number",
      helpUrl: "",
    });
  },
};

Blockly.Blocks["uno_tcs34725_detect"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      tooltip: "",
      message0: "cảm biến màu sắc phát hiện màu %1",
      args0: [
        {
          type: "field_dropdown",
          name: "color",
          options: [
            ["trắng", "w"],
            ["đen", "d"],
            ["đỏ", "r"],
            ["xanh lá (green)", "g"],
            ["xanh dương (blue)", "b"],
            ["vàng", "y"]
          ],
        }
      ],
      output: "Boolean",
      helpUrl: "",
    });
  },
};

Blockly.Python["uno_tcs34725_read"] = function (block) {
  var RGB = block.getFieldValue("RGB");
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  var code = "tcs34725.read_color('" + RGB + "')";
  return [code, Blockly.Python.ORDER_NONE];
};

Blockly.Python["uno_tcs34725_detect"] = function (block) {
  var color = block.getFieldValue("color");
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  var code = "tcs34725.detect('" + color + "')";
  return [code, Blockly.Python.ORDER_NONE];
};


// ============================================================
// NEW BLOCKS
// ============================================================

// ---- 1. Trạng thái: is_ready --------------------------------

Blockly.Blocks["tcs34725_is_ready"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: đã kết nối?",
      output: "Boolean",
      tooltip:
        "Kiểm tra xem cảm biến màu sắc có đang kết nối và hoạt động bình thường không.\n" +
        "Trả về TRUE nếu cảm biến sẵn sàng, FALSE nếu không tìm thấy.\n" +
        "Dùng khối này ở đầu chương trình để kiểm tra trước khi đọc màu.\n" +
        "Ví dụ: nếu (cảm biến đã kết nối?) thì ... không thì in ra 'Lỗi kết nối'",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_is_ready"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return ["tcs34725.is_ready()", Blockly.Python.ORDER_NONE];
};


// ---- 2. Calibration: ghi nhớ trắng -------------------------

Blockly.Blocks["tcs34725_calibrate_white"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: ghi nhớ màu TRẮNG",
      previousStatement: null,
      nextStatement: null,
      tooltip:
        "Dạy cảm biến nhận biết màu TRẮNG theo điều kiện ánh sáng thực tế.\n" +
        "CÁCH DÙNG: Đặt cảm biến lên bề mặt TRẮNG (hoặc nền sáng nhất), rồi chạy khối này.\n" +
        "Nên dùng cùng với khối 'ghi nhớ màu ĐEN' để cảm biến hoạt động chính xác hơn.\n" +
        "Thực hiện hiệu chuẩn mỗi khi thay đổi môi trường ánh sáng.",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_calibrate_white"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return "tcs34725.calibrate_white()\n";
};


// ---- 3. Calibration: ghi nhớ đen ----------------------------

Blockly.Blocks["tcs34725_calibrate_black"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: ghi nhớ màu ĐEN",
      previousStatement: null,
      nextStatement: null,
      tooltip:
        "Dạy cảm biến nhận biết màu ĐEN (bề mặt tối nhất) theo điều kiện thực tế.\n" +
        "CÁCH DÙNG: Đặt cảm biến lên bề mặt ĐEN (hoặc nền tối nhất), rồi chạy khối này.\n" +
        "Nên dùng cùng với khối 'ghi nhớ màu TRẮNG' để cảm biến hoạt động chính xác hơn.\n" +
        "Thực hiện hiệu chuẩn mỗi khi thay đổi môi trường ánh sáng.",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_calibrate_black"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return "tcs34725.calibrate_black()\n";
};


// ---- 4. Nhận diện màu: get_color_name -----------------------

Blockly.Blocks["tcs34725_get_color_name"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: tên màu đang đọc",
      output: "String",
      tooltip:
        "Trả về tên màu của vật đang đặt trước cảm biến dưới dạng chữ (tiếng Việt).\n" +
        "Các màu có thể trả về: 'đỏ', 'cam', 'vàng', 'xanh lá',\n" +
        "'xanh dương', 'tím', 'hồng', 'trắng', 'đen', 'không xác định'.\n" +
        "Sử dụng HSV nên ít bị ảnh hưởng bởi cường độ ánh sáng hơn.\n" +
        "Ví dụ: nếu (tên màu đang đọc) = 'đỏ' thì robot rẽ phải",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_get_color_name"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return ["tcs34725.get_color_name()", Blockly.Python.ORDER_NONE];
};


// ---- 5. Dò line: on_dark_surface ----------------------------

Blockly.Blocks["tcs34725_on_dark"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: đang trên vạch TỐI?",
      output: "Boolean",
      tooltip:
        "Trả về TRUE nếu cảm biến đang nằm trên vạch tối (màu đen hoặc sẫm).\n" +
        "Dùng cho robot dò line: khi TRUE nghĩa là cảm biến đang trên vạch.\n" +
        "ĐỂ CHÍNH XÁC HƠN: Chạy 'ghi nhớ màu TRẮNG' và 'ghi nhớ màu ĐEN' trước.\n" +
        "Nếu chưa hiệu chuẩn, cảm biến vẫn hoạt động nhưng kém chính xác hơn.\n" +
        "Gợi ý: dùng kết hợp với khối '% sáng/tối' để điều khiển robot mượt hơn.",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_on_dark"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return ["tcs34725.on_dark_surface()", Blockly.Python.ORDER_NONE];
};


// ---- 6. Dò line: on_light_surface ---------------------------

Blockly.Blocks["tcs34725_on_light"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: đang trên nền SÁNG?",
      output: "Boolean",
      tooltip:
        "Trả về TRUE nếu cảm biến đang nằm trên bề mặt sáng (màu trắng hoặc nhạt).\n" +
        "Dùng cho robot dò line: khi TRUE nghĩa là cảm biến đang ở ngoài vạch.\n" +
        "ĐỂ CHÍNH XÁC HƠN: Chạy 'ghi nhớ màu TRẮNG' và 'ghi nhớ màu ĐEN' trước.\n" +
        "Nếu chưa hiệu chuẩn, cảm biến vẫn hoạt động nhưng kém chính xác hơn.\n" +
        "Gợi ý: dùng kết hợp với khối '% sáng/tối' để điều khiển robot mượt hơn.",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_on_light"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return ["tcs34725.on_light_surface()", Blockly.Python.ORDER_NONE];
};


// ---- 7. Dò line: line_position_percent ----------------------

Blockly.Blocks["tcs34725_line_position"] = {
  init: function () {
    this.jsonInit({
      colour: TCS34725ColorBlock,
      message0: "cảm biến màu sắc: % sáng/tối (0=đen, 100=trắng)",
      output: "Number",
      tooltip:
        "Trả về con số từ 0 đến 100 cho biết bề mặt bên dưới sáng hay tối đến mức nào.\n" +
        "  0   = hoàn toàn trên vạch đen\n" +
        "  50  = cảm biến nằm đúng mép vạch (nửa trên vạch, nửa ngoài)\n" +
        "  100 = hoàn toàn trên nền trắng\n" +
        "DÙNG ĐỂ: Điều khiển tốc độ 2 bánh robot theo tỉ lệ (PID đơn giản),\n" +
        "giúp robot bám line mượt hơn so với chỉ dùng khối TRUE/FALSE.\n" +
        "Ví dụ: tốc độ bánh trái = 50 + (% sáng/tối - 50), bánh phải ngược lại.\n" +
        "ĐỂ CHÍNH XÁC: Chạy 'ghi nhớ màu TRẮNG' và 'ghi nhớ màu ĐEN' trước.",
      helpUrl: "",
    });
  },
};

Blockly.Python["tcs34725_line_position"] = function (block) {
  Blockly.Python.definitions_['import_tcs34725'] = 'from tcs34725 import *';
  Blockly.Python.definitions_['init_tcs34725'] = 'tcs34725 = TCS34725()';
  return ["tcs34725.line_position_percent()", Blockly.Python.ORDER_NONE];
};
