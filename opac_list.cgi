#!/usr/bin/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")


def indtd(str)
  printf("<td>%s</td>\n", CGI.escapeHTML(str))
end

def stitle(str)
  return "(title like " + str + " or titleheading like " + str + ") "
end

def sauthor(str)
  return "(author like " + str + " or authorheading like " + str + ") "
end

def spub(str)
  return "(pub like " + str + ") "
end

def sseries(str)
  return "(series like " + str + ") "
end


c = CGI.new
db = SQLite3::Database.new("opac.db")


# ここからSQL文構成

sqltext = "select * from opac "

s_any = c["any"]

if s_any != ""
  sqltext += "where "
  any_array = s_any.split(/[\s\p{blank}]+/)
  last_index = any_array.length - 1
  i = 0
  any_array.each{ |sword|
    sw = "'%" + sword + "%'"
    sqltext += "("
    sqltext += "nbc like " + sw
    sqltext += " or "
    sqltext += "isbn like " + sw
    sqltext += " or "
    sqltext += "title like " + sw
    sqltext += " or "
    sqltext += "author like " + sw
    sqltext += " or "
    sqltext += "ed like " + sw
    sqltext += " or "
    sqltext += "pub like " + sw
    sqltext += " or "
    sqltext += "date like " + sw
    sqltext += " or "
    sqltext += "phys like " + sw
    sqltext += " or "
    sqltext += "series like " + sw
    sqltext += " or "
    sqltext += "note like " + sw
    sqltext += " or "
    sqltext += "titleheading like " + sw
    sqltext += " or "
    sqltext += "authorheading like " + sw
    sqltext += " or "
    sqltext += "holdingsrecord like " + sw
    sqltext += " or "
    sqltext += "holdingloc like " + sw
    sqltext += ") "

    if i < last_index
      if c["anysel"] == "and"
        sqltext += "and "
      else
        sqltext += "or "
      end
      i += 1
    end
  }

else

  fd = Hash.new

  if c["title"] != ""
    fd["title"] = "'%" + c["title"] + "%'"
  end
  if c["author"] != ""
    fd["author"] = "'%" + c["author"] + "%'"
  end
  if c["pub"] != ""
    fd["pub"] = "'%" + c["pub"] + "%'"
  end
  if c["series"] != ""
    fd["series"] = "'%" + c["series"] + "%'"
  end

  imax = fd.length - 1
  i = 0

  if imax >= 0
    sqltext += "where "
  end

  fd.each{ |key, value|
    if key == "title"
      sqltext += stitle(value)
    elsif key == "author"
      sqltext += sauthor(value)
    elsif key == "pub"
      sqltext += spub(value)
    elsif key == "series"
      sqltext += sseries(value)
    end
      
      if i < imax
        sqltext += "and "
      end
      i += 1
  }
end

sqltext += ";"

# ここまでSQL文構成

# ここからSQL文実行

rows = Array.new

db.transaction{
  db.execute(sqltext){ |row|
    rows.push(row)
  }
}

# ここまでSQL文実行




# ここから表示

print("Content-Type: text/html; charset=utf-8\n")
print("\n")
print("<!DOCTYPE html>\n")
print("<html>\n")
print("<head>\n")
print("<link rel='stylesheet' type='text/css' href='css.css' />")
print("<title>opac</title>\n")
print("</head>\n")
print("<body>\n")

print(<<"EOS")
<div id='center'>
<h1>やまじゅんOPAC</h1>
  <form method='POST' action='opac_list.cgi'>
  検索語を入力<br>
  <table>
EOS

printf("<tr><td>簡易検索</td><td><input type='text' name='any' size='20' value='%s'>", c["any"])

if c["anysel"] == "and"
  print("<select name='anysel'>
      <option value='and' selected>AND</option>
      <option value='or'>OR</option>
    </select>
  </td></tr>")
else
  print("<select name='anysel'>
      <option value='and'>AND</option>
      <option value='or' selected>OR</option>
    </select>
  </td></tr>")
end

printf("<tr><td>タイトル</td><td><input type='text' name='title' size='20' value='%s'></td></tr>
  <tr><td>著者</td><td><input type='text' name='author' size='20' value='%s'></td></tr>
  <tr><td>出版社</td><td><input type='text' name='pub' size='20' value='%s'></td></tr>
  <tr><td>シリーズ</td><td><input type='text' name='series' size='20' value='%s'></td></tr>", c["title"], c["author"], c["pub"], c["series"])

print(<<"EOS")
  </table>
  <input type='submit' value='検索'><input type='reset' value='空にする'>
  </form>
  </div>
  <br>
EOS




printf("<div>検索件数: %d件</div>\n", rows.length)


print("<table border='1'>\n")
print("<tr>\n")
print("<th>No</th>\n")
print("<th>NBC</th>\n")
print("<th>ISBN</th>\n")
print("<th>タイトル</th>\n")
print("<th>著者</th>\n")
print("<th>出版社</th>\n")
print("<th>出版年月</th>\n")
print("</tr>")

i = 0
rows.each{ |row|

  i = i + 1

  if(i % 2 == 0)
    print("<tr bgcolor='#ccddcc'>")
  else
    print("<tr bgcolor='#eeffee'>")
  end
  indtd(i.to_s)
  indtd(row[0].to_s)
  indtd(row[1].to_s)
  indtd(row[2].to_s)
  indtd(row[3].to_s)
  indtd(row[5].to_s)
  indtd(row[6].to_s)
  print("</tr>")

}

print("</table>\n")

print("</body>\n")
print("</html>\n")


# ここまで表示

db.close



