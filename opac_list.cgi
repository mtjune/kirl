#!/usr/bin/ruby
# -*- coding: utf-8 -*-

require("sqlite3")
require("cgi")

def indirow(r0, r2, r3, r4, r5, ii)
    if(ii % 2 == 0)
      print("<tr bgcolor='#eeffee'>")
    else
      print("<tr bgcolor='#ccddcc'>")
    end
    printf("<td>%s</td>\n", CGI.escapeHTML(r0))
    printf("<td>%s</td>\n", CGI.escapeHTML(r1))
    printf("<td>%s</td>\n", CGI.escapeHTML(r2))
    printf("<td>%s</td>\n", CGI.escapeHTML(r3))
    printf("<td>%s</td>\n", CGI.escapeHTML(r4))
    printf("<td>%s</td>\n", CGI.escapeHTML(r5))
    print("</tr>")
end



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
  sqltext = "select * from opac1 where title like :title and auther like :author and pub like :publication ;"
  s_title = "%" + c["title"] + "%"
  s_author = "%" + c["author"] + "%"
  s_publication = "%" + c["publication"] + "%"
  i = 1
  db.execute(sqltext, :title=>s_title, :author=>s_author, :publication=>s_publication){ |row|
    i = i + 1

    if(i % 2 == 0)
      print("<tr bgcolor='#eeffee'>")
    else
      print("<tr bgcolor='#ccddcc'>")
    end
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



