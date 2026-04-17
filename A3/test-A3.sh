#! /bin/bash

passed=0
total=0

run_test() {
    local name="$1"
    local expected="$2"
    shift 2

    ((total++))

    diff_output=$("$@" | diff - "$expected")
    if [ $? -eq 0 ]; then
        echo "✅ $name"
        ((passed++))
    else
        echo "❌ $name"
        echo "$diff_output"
    fi
}

# --- tests ---
run_test "Manhattan-testHV1" "Manhattan-testHV1.out" python3 juwei95-Manhattan.py Manhattan-testHV1.in
run_test "Manhattan-testHV2" "Manhattan-testHV2.out" python3 juwei95-Manhattan.py -t Manhattan-testHV2.in
run_test "Manhattan-testHV3" "Manhattan-testHV3.out" python3 juwei95-Manhattan.py -t Manhattan-testHV3.in
run_test "Manhattan-testHVD1" "Manhattan-testHVD1.out" python3 juwei95-Manhattan.py -d Manhattan-testHVD1.in
run_test "Manhattan-testHVD2" "Manhattan-testHVD2.out" python3 juwei95-Manhattan.py -d Manhattan-testHVD2.in

# --- summary ---
failed=$((total - passed))
echo "Passed $passed / $total"

exit $failed