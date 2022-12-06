#!/usr/bin/perl
use warnings;
use strict;

my $filename = 'day5.txt';

open(FH, '<', $filename) or die $!;

my @array;
my $needs_init = 1;
my $is_part_1 = 0;

while(<FH>){
    if(substr($_, 1, 1) =~ "1") {
        last;
    }

    my $line_line = length($_);
    my $len = int(($line_line - 1) / 4);

    if($needs_init) {
        for my $i (0..$len-1) {
            $array[$i] = "";
        }
        $needs_init = 0;
    }

    for( my $i = 1; $i < $line_line; $i = $i + 4 ) {
        my $char = substr($_, $i, 1);
        if ($char ne " ") {
            my $index = int(($i - 1) / 4);
            @array[$index] = @array[$index].$char;
        }
    }
}

my $len = @array;
for my $i (0..$len-1) {
    print  "$i @array[$i]\n";
}

while(<FH>){
    my $line_line = length($_);
    if ($line_line <= 1) {
        next;
    }

    if ($_ =~ /^move (\d+) from (\d+) to (\d+)$/) {

        my $from = $2 - 1;
        my $to = $3 - 1;
        my $move = $1;
        print "move $move from $from to $to\n";

        my $from_str = @array[$from];
        my $to_move = substr($from_str, 0, $move);
        @array[$from] = substr($from_str, $move, length($from_str) - $move);


        if($is_part_1) {
            @array[$to] = reverse($to_move).@array[$to];
        } else {
            @array[$to] = $to_move.@array[$to];
        }

        print "to_move $to_move from: $from_str to: @array[$to]\n";
    } else {
        print "Parsing Error";
        exit;
    }

    for my $i (0..$len-1) {
        print  "$i @array[$i]\n";
    }

}
close(FH);

for my $i (0..$len-1) {
    print  substr(@array[$i], 0, 1);
}
print "\n";