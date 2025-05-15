<?php
// download-template.php: Xuất mẫu Excel (.xlsx) cho upload game

// Kiểm tra thư viện PhpSpreadsheet
if (!file_exists(__DIR__ . '/vendor/autoload.php')) {
    header('Content-Type: text/plain; charset=utf-8');
    echo "Thư viện PhpSpreadsheet không có sẵn. Vui lòng chạy 'composer require phpoffice/phpspreadsheet'.";
    exit;
}
require __DIR__ . '/vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\Spreadsheet;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;

// Tạo Spreadsheet và thiết lập tiêu đề cột
$spreadsheet = new Spreadsheet();
$sheet = $spreadsheet->getActiveSheet();
$sheet->setCellValue('A1', 'Tên Game');
$sheet->setCellValue('B1', 'Mô Tả Game');
$sheet->setCellValue('C1', 'iframe URL');
$sheet->setCellValue('D1', 'Danh Mục');
$sheet->setCellValue('E1', 'Định Dạng Hình');

// Xuất file
header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
header('Content-Disposition: attachment;filename="game-template.xlsx"');
header('Cache-Control: max-age=0');

$writer = new Xlsx($spreadsheet);
$writer->save('php://output');
exit; 