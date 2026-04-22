#!/bin/bash

g++ test_Manhattan.cpp -O2 -o manhattan

passed=0
total=0

run_test() {
    local name="$1"
    local expected="$2"
    shift 2

    ((total++))

    start=$(date +%s%N)

    diff_output=$("$@" | diff - "$expected")
    status=$?

    end=$(date +%s%N)
    runtime_ns=$((end - start))
    runtime_ms=$((runtime_ns / 1000000))

    if [ $status -eq 0 ]; then
        echo "✅ $name (${runtime_ms} ms)"
        ((passed++))
    else
        echo "❌ $name (${runtime_ms} ms)"
        echo "$diff_output"
    fi
}

# --- tests ---
run_test "Manhattan-testHV1" "Manhattan-testHV1.out" python3 juwei95-Manhattan.py Manhattan-testHV1.in
run_test "Manhattan-testHV2" "Manhattan-testHV2.out" python3 juwei95-Manhattan.py -t Manhattan-testHV2.in
run_test "Manhattan-testHV3" "Manhattan-testHV3.out" python3 juwei95-Manhattan.py -t Manhattan-testHV3.in
run_test "Manhattan-testHVD1" "Manhattan-testHVD1.out" python3 juwei95-Manhattan.py -d Manhattan-testHVD1.in
run_test "Manhattan-testHVD2" "Manhattan-testHVD2.out" python3 juwei95-Manhattan.py -d Manhattan-testHVD2.in
run_test "Manhattan-testHV1" "Manhattan-testHV1.out" python3 juwei95-Manhattan.py -b Manhattan-testHV1.in
run_test "Manhattan-testHV2" "Manhattan-testHV2.out" python3 juwei95-Manhattan.py -b -t Manhattan-testHV2.in
run_test "Manhattan-testHV3" "Manhattan-testHV3.out" python3 juwei95-Manhattan.py -b -t Manhattan-testHV3.in
run_test "Manhattan-testHVD1" "Manhattan-testHVD1.out" python3 juwei95-Manhattan.py -b -d Manhattan-testHVD1.in
run_test "Manhattan-testHVD2" "Manhattan-testHVD2.out" python3 juwei95-Manhattan.py -b -d Manhattan-testHVD2.in
run_test "Manhattan-testHV1" "Manhattan-testHV1.out" ./manhattan Manhattan-testHV1.in
run_test "Manhattan-testHV2" "Manhattan-testHV2.out" ./manhattan Manhattan-testHV2.in -t
run_test "Manhattan-testHV3" "Manhattan-testHV3.out" ./manhattan Manhattan-testHV3.in -t
run_test "Manhattan-testHVD1" "Manhattan-testHVD1.out" ./manhattan Manhattan-testHVD1.in -d
run_test "Manhattan-testHVD2" "Manhattan-testHVD2.out" ./manhattan Manhattan-testHVD2.in -d

# --- summary ---
failed=$((total - passed))
echo "Passed $passed / $total"

exit $failed
