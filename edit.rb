#!/usr/bin/ruby
# -*- coding: utf-8 -*-

nbc = ""
isbn = ""
tr = ""
pub = ""

io = open("jbisc.txt", "r")

while true
  line = io.gets
  if line == nil
    break
  end

  if /^NBC:\s+/ =~ line
    nbc = line.chomp.sub(/^NBC:\s+/, "")
  elsif /^ISBN:\s+/ =~ line
    isbn = line.chomp.sub(/^ISBN:\s+/, "")
  elsif /^TR:\s+/ =~ line
    tr = line.chomp.sub(/^TR:\s+/, "")
    if /\s+\/\s+/ =~tr
      tr.sub!(/\s+\/\s+/, "|")
    else
      tr = tr + "|"
    end
  elsif /^PUB:\s+/ =~ line
    pub = line.chomp.sub(/^PUB:\s+/, "")
    if /,\s+/ =~pub
      pub.sub!(/,\s+/, "|")
    else
      pub = pub + "|"
    end
  elsif /^\*/ =~ line
    printf("%s|%s|%s|%s\n", nbc, isbn, tr, pub)
    nbc = ""
    isbn = ""
    tr = ""
    pub = ""
  end
end

printf("%s|%s|%s|%s\n", nbc, isbn, tr, pub)

io.close
