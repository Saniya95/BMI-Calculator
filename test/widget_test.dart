import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:bmi_calculator_app/main.dart';

void main() {
  testWidgets('Calculates BMI and shows the right category', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const BMICalculatorApp());

    final fields = find.byType(TextField);
    expect(fields, findsNWidgets(3));

    await tester.enterText(fields.at(0), '5');
    await tester.enterText(fields.at(1), '8');
    await tester.enterText(fields.at(2), '70');

    await tester.tap(find.text('Calculate'));
    await tester.pump();

    expect(find.text('BMI: 23.46'), findsOneWidget);
    expect(find.text('Category: Normal'), findsOneWidget);
  });
}
