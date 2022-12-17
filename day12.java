
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import java.util.Arrays;

import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class day12 {
    private final char[][] mapIn;
    private final int[][] shortestFound;
    private final boolean[][] visited;
    private final int nI, nJ, sI, sJ, eI, eJ;

    {
        try {
            Stream<String> linesIn = Files.readString(Path.of("day12.txt")).lines();
            mapIn = linesIn.map(String::toCharArray).toArray(char[][]::new);
            nI = mapIn.length;
            nJ = mapIn[0].length;
            shortestFound = new int[nI][nJ];
            for(int i = 0; i < mapIn.length; i++) {
                Arrays.fill(shortestFound[i], Integer.MAX_VALUE);
            }
            visited = new boolean[nI][nJ];

            final int sIndex = IntStream.range(0, nI*nJ).filter(i -> mapIn[i/nJ][i%nJ] == 'S').findAny().orElseThrow(() -> new IllegalArgumentException("No Start"));
            sI = sIndex/nJ;
            sJ = sIndex%nJ;

            final int eIndex = IntStream.range(0, nI*nJ).filter(i -> mapIn[i/nJ][i%nJ] == 'E').findAny().orElseThrow(() -> new IllegalArgumentException("No End"));
            eI = eIndex/nJ;
            eJ = eIndex%nJ;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private int charDistance(final char c1, final char c2) {
        if(c1 == 'S' && c2 == 'a') {
            return 1;
        } else if (c1 == 'z' && c2 == 'E') {
            return 1;
        } else if (c1 != 'z' && c2 == 'E') {
            return Integer.MAX_VALUE;
        } else {
            return (int)c2 - (int)c1;
        }
    }

    private int part1() {
        final PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(i -> i[2]));
        pq.add(new int[]{sI, sJ, -1});
        while (!pq.isEmpty()) {
            final int[] ij = pq.poll();
            final int i = ij[0];
            final int j = ij[1];
            final int currentPathLength = ij[2];
            final char c = mapIn[i][j];

            if (visited[i][j]) {
                continue;
            }
            visited[i][j] = true;

            if (c == 'E') {
                shortestFound[i][j] = currentPathLength - 1;
                continue;
            }

            shortestFound[i][j] = currentPathLength;
            final int cpp1 = currentPathLength + 1;

            Stream.of(new int[]{i+1, j, cpp1}, new int[]{i-1, j, cpp1}, new int[]{i, j+1, cpp1}, new int[]{i, j-1, cpp1}).filter(ijNext -> {
                final int iNext = ijNext[0];
                final int jNext = ijNext[1];
                return iNext >= 0 &&
                        iNext < nI &&
                        jNext >= 0 &&
                        jNext < nJ &&
                        charDistance(c, mapIn[iNext][jNext]) <= 1;
            }).forEach(pq::add);
        }

        return shortestFound[eI][eJ];
    }


    private int part2() {

        int k = 0;
        final PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(i -> i[2]));

        visited[sI][sJ] = true;
        IntStream.range(0, nI*nJ).filter(i -> mapIn[i/nJ][i%nJ] == 'a').forEach(i -> {
            final int iA = i/nJ;
            final int jA = i%nJ;
            pq.add(new int[]{iA, jA, 0});
        });

        int min = Integer.MAX_VALUE;

        while (!pq.isEmpty()) {
            final int[] ij = pq.poll();
            final int i = ij[0];
            final int j = ij[1];
            final int currentPathLength = ij[2];
            final char c = mapIn[i][j];

            if (visited[i][j]) {
                continue;
            }
            visited[i][j] = true;

            if (shortestFound[i][j] != Integer.MAX_VALUE) {
                System.out.println("i: " + i + ", j: " + j + ", " + c + ", shortestFound: " + shortestFound[i][j] + ", currentPathLength: " + currentPathLength);
            }

            shortestFound[i][j] = currentPathLength;
            if (c == 'E') {
                min = Math.min(min, currentPathLength);
                continue;
            }

            final int cpp1 = currentPathLength + 1;

            Stream.of(new int[]{i+1, j, cpp1}, new int[]{i-1, j, cpp1}, new int[]{i, j+1, cpp1}, new int[]{i, j-1, cpp1}).filter(ijNext -> {
                final int iNext = ijNext[0];
                final int jNext = ijNext[1];
                return iNext >= 0 &&
                        iNext < nI &&
                        jNext >= 0 &&
                        jNext < nJ &&
                        charDistance(c, mapIn[iNext][jNext]) <= 1;
            }).forEach(pq::add);
        }

        return shortestFound[eI][eJ] - 2;
    }

    public static void main(String[] args) {
        final day12 d12 = new day12();
        //System.out.println(d12.part1());
        System.out.println(d12.part2());
    }
}