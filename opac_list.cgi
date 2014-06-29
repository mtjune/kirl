#!/usr/bin/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")

c = CGI.new
db = SQLite3::Database.new("opac.db")




print("Content-Type: text/html; charset=utf-8\n")
print("\n")
print("<!DOCTYPE html>\n")
print("<html>\n")
print("<head>\n")
print("<title>opac</title>\n")
print("</head>\n")
print("<body>\n")

print("<table border='1'>\n")
print("<tr>\n")
print("<th>NBC</th>\n")
print("<th>ISBN</th>\n")
print("<th>タイトル</th>\n")
print("<th>著者</th>\n")
print("<th>出版社</th>\n")
print("<th>出版年月</th>\n")
print("</tr>")

db.transaction{
  word = "%" + c["searchword"] + "%"
  db.execute("select * from opac1 where title like ? or auther like ?;", word, word){ |row|
    # indbib(row[0], row[1], row[2], row[3], row[4], row[5])
    print("<tr>")
    printf("<td>%s</td>\n", CGI.escapeHTML(row[0].to_s))
    printf("<td>%s</td>\n", CGI.escapeHTML(row[1].to_s))
    printf("<td>%s</td>\n", CGI.escapeHTML(row[2].to_s))
    printf("<td>%s</td>\n", CGI.escapeHTML(row[3].to_s))
    printf("<td>%s</td>\n", CGI.escapeHTML(row[4].to_s))
    printf("<td>%s</td>\n", CGI.escapeHTML(row[5].to_s))
    print("</tr>")
  }
}
print("</table>\n")

print("</body>\n")
print("</html>\n")

db.close


# ここからメソッド定義

# def indbib(r0, r1, r2, r3, r4, r5)
#   print("<tr>")
#   printf("<td>%s</td>\n", CGI.escapeHTML(r0.to_s))
#   printf("<td>%s</td>\n", CGI.escapeHTML(r1.to_s))
#   printf("<td>%s</td>\n", CGI.escapeHTML(r2.to_s))
#   printf("<td>%s</td>\n", CGI.escapeHTML(r3.to_s))
#   printf("<td>%s</td>\n", CGI.escapeHTML(r4.to_s))
#   printf("<td>%s</td>\n", CGI.escapeHTML(r5.to_s))
#   print("</tr>")
# end
