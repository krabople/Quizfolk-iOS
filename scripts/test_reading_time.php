<?php
require __DIR__.'/../backend/questions.php';
function check_reading(string $prompt,int $expected):void {
    if(question_reading_seconds($prompt)!==$expected)throw new RuntimeException('Reading allowance mismatch');
}
check_reading('',3);
check_reading('Which planet is known as the Red Planet?',3);
check_reading(str_repeat('word ',12),3);
check_reading(str_repeat('word ',30),9);
check_reading(str_repeat('word ',60),19);
check_reading(str_repeat('x',90),4);
check_reading(str_repeat('🌿',90),4);
check_reading("  one\t two\nthree\u{00A0}four  ",3);
echo "Adaptive reading boundaries and Unicode passed.\n";
