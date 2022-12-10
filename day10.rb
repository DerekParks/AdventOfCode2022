#!/usr/bin/env ruby

x = Array([1])

File.readlines('day10.txt').each do |line|
    if line.start_with?('noop')
        puts("noop")
        x.push(x.last)
    elsif line.start_with?('addx')
        value = line[5..-1].to_i
        puts("addx #{value}")
        x.push(x.last)
        x.push(x.last + value)
    end
end

cycle_start = 20
cycle_space = 40

result = 0
for i in 0..x.length-1
    puts("#{i}: #{x[i]}")
    if (i != 0) && ((i - cycle_start) % cycle_space  == 0)
        this_result = i * x[i-1]
        result += this_result
        puts("\t #{x[i-1]} #{this_result} #{result}")
    end
end

puts("part1: #{result}")

# part2
pixels = []
for i in 0..5
    pixels.push(Array.new(40, false))
end

for reg_pos in 0..x.length-1
    reg_value = x[reg_pos]

    i = reg_pos / 40;
    j = reg_pos % 40;

    puts("#{reg_pos}: #{reg_value} #{i} #{j}")
    if j == (reg_value -1) || j == reg_value || j == (reg_value + 1)
        pixels[i][j] = true
    end
end

for i in 0..5
    for j in 0..39
        if pixels[i][j]
            print("#")
        else
            print(".")
        end
    end
    puts("")
end
