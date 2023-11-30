function fixedHex(number, length) {
  var str = number.toString(16).toUpperCase();
  while (str.length < length) str = "0" + str;
  return str;
}

export default function unicodeLiteral(str) {
  /*  convert unicode character to string literal
  
  such as: 󰄛 -> "\uDB80\uDD1B"
  
    Refs:
      https://stackoverflow.com/a/10937446
     */
  var i;
  var result = "";
  for (i = 0; i < str.length; ++i) {
    if (str.charCodeAt(i) > 128)
      result += "\\u" + fixedHex(str.charCodeAt(i), 4);
    else result += str[i];
  }

  return result;
}
