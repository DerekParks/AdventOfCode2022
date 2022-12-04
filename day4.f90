PROGRAM day4
    IMPLICIT none

    INTERFACE 
        SUBROUTINE To_Int(some_str, int_out)
            CHARACTER(len=100), INTENT(IN) :: some_str
            INTEGER, INTENT(OUT) :: int_out
        END SUBROUTINE To_Int
    END INTERFACE

    CHARACTER(len=200) :: line
    CHARACTER(len=100) :: line_elf1
    CHARACTER(len=100) :: line_elf2

    INTEGER :: elf1_low
    INTEGER :: elf1_high
    INTEGER :: elf2_low
    INTEGER :: elf2_high

    CHARACTER(len=50), PARAMETER :: file_name = 'day4.txt'
    INTEGER, PARAMETER :: fd = 42
    INTEGER :: count_pt1 = 0
    INTEGER :: count_pt2 = 0

    INTEGER :: len = 0
    INTEGER :: ios = 0

    INTEGER :: comma_i
    INTEGER :: dash_i

    open(unit = fd, file=file_name, status="old")

    DO
        READ(fd, "(A)", iostat=ios) line
        IF (ios/=0) EXIT

        len = len + 1

        comma_i = INDEX(line, ",")
        line_elf1 = line(:comma_i-1)
        line_elf2 = line(comma_i+1:)

        dash_i = INDEX(line_elf1, "-")

        CALL To_Int(line_elf1(:dash_i-1), elf1_low)
        CALL To_Int(line_elf1(dash_i+1:), elf1_high)

        dash_i = INDEX(line_elf2, "-")

        CALL To_Int(line_elf2(:dash_i-1), elf2_low)
        CALL To_Int(line_elf2(dash_i+1:), elf2_high)

        PRINT *, elf1_low, elf1_high, elf2_low, elf2_high

        IF (elf1_low > elf1_high) THEN
            PRINT *, "Illegal Input! Elf 1 is out of order!"
            EXIT
        END IF

        IF (elf2_low > elf2_high) THEN
            PRINT *, "Illegal Input! Elf 2 is out of order!"
            EXIT
        END IF

        IF (elf1_high >= elf2_low .AND. elf2_high >= elf1_low) THEN
            count_pt2 = count_pt2 + 1
        END IF
        IF (elf1_low >= elf2_low .AND. elf1_high <= elf2_high ) THEN
            count_pt1 = count_pt1 + 1
        ELSE IF (elf2_low >= elf1_low .AND. elf2_high <= elf1_high ) THEN
            count_pt1 = count_pt1 + 1
        END IF
    END DO

    CLOSE(fd)

    PRINT *, 'Completely overlapping:', count_pt1, "Some overlap:", count_pt2 , "Length", len
END PROGRAM day4


SUBROUTINE To_Int(some_str, int_out)
    IMPLICIT none

    CHARACTER(len=100), INTENT(IN) :: some_str
    INTEGER, INTENT(OUT) :: int_out
    INTEGER :: ios = 0

    read (some_str,'(I2)', iostat=ios) int_out
    IF (ios/=0) read (some_str,'(I1)', iostat=ios) int_out
    IF (ios/=0) int_out = -1
END SUBROUTINE To_Int