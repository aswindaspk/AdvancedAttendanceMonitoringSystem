import 'dart:convert';

import 'package:ats/home.dart';
import 'package:ats/parent_subject_attendance.dart';
import 'package:ats/subject_attendance.dart';
import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:month_picker_dialog/month_picker_dialog.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Leave Request Form',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PAttendanceNew(),
    );
  }
}

class PAttendanceNew extends StatefulWidget {
  @override
  _PAttendanceNewState createState() => _PAttendanceNewState();
}

List<String> list = <String>[];

class _PAttendanceNewState extends State<PAttendanceNew> {
  _PAttendanceNewState() {
    getdata();
    getmonthly();
    gettotal();
  }

  DateTime selectedDate = DateTime.now();
  DateTime selectedMonth = DateTime.now();
  bool isDatePicked = false;
  bool isMonthPicked = false;
  String h1_ = '';
  String h2_ = '';
  String h3_ = '';
  String h4_ = '';
  String h5_ = '';
  String h6_ = '';
  String total_ = '';
  String percentage_ = '';
  String ttl_ = '';
  String m_ = '';
  String mv_ = '';



  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate, firstDate: DateTime(2010),
      lastDate: DateTime(2030),

      // 000000,
    );
    if (picked != null && picked != selectedDate)
      setState(() {
        selectedDate = picked;
        isDatePicked = true;
        isMonthPicked = false;
        getdata();
        gettotal();


      });
  }




  Future<void> _selectMonthYear(BuildContext context) async {
    final DateTime? picked = await showMonthPicker(
      context: context,
      initialDate: selectedDate,
      firstDate: DateTime(2010),
      lastDate: DateTime(2030),
    );

    if (picked != null) {
      setState(() {
        isDatePicked = false;
        selectedMonth = picked;
        isMonthPicked = true;

        getmonthly();
      });
    }
  }





  Color primary = const Color(0xffeef444c);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                alignment: Alignment.centerLeft,
                margin: const EdgeInsets.only(left:20, top: 35, bottom: 8),
                child: Text(
                  "Attendance",
                  style: TextStyle(fontFamily: "Nexa_bold", fontSize: 30),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(top: 12, left: 40, right: 40),
                height: 100,
                decoration: const BoxDecoration(
                  color: Colors.white,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black26,
                      blurRadius: 10,
                      offset: Offset(2, 2),
                    )
                  ],
                  borderRadius: BorderRadius.all(Radius.circular(20)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Text(
                              "Pick Date",
                              style: TextStyle(
                                fontFamily: "Nexa_light",
                                fontSize: 20,
                                color: Colors.black54,
                              ),
                            ),
                            TextButton(
                              onPressed: () => _selectDate(context),
                              child: Text(
                                '${selectedDate.day}/${selectedDate.month}/${selectedDate.year}',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: "Nexa_bold",
                                  color: primary,
                                ),
                              ),
                            ),

                          ],
                        )),

                  ],
                ),

              ),
              Container(
                margin: const EdgeInsets.only(top: 12, left: 40, right: 40),
                height: 30,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Text(
                              "OR",
                              style: TextStyle(
                                fontFamily: "Nexa_light",
                                fontSize: 20,
                                color: Colors.black54,
                              ),
                            ),
                          ],
                        )),

                  ],
                ),
              ),
              Container(
                margin: const EdgeInsets.only(top: 12, left: 40, right: 40),
                height: 100,
                decoration: const BoxDecoration(
                  color: Colors.white,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black26,
                      blurRadius: 10,
                      offset: Offset(2, 2),
                    )
                  ],
                  borderRadius: BorderRadius.all(Radius.circular(20)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Text(
                              "Pick Month",
                              style: TextStyle(
                                fontFamily: "Nexa_light",
                                fontSize: 20,
                                color: Colors.black54,
                              ),
                            ),
                            TextButton(
                              onPressed: () => _selectMonthYear(context),
                              child: Text(
                                '${selectedDate.month}/${selectedDate.year}',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontFamily: "Nexa_bold",
                                  color: primary,
                                ),
                              ),
                            ),
                          ],
                        )),

                  ],
                ),
              ),

              if (isDatePicked)
                Container(
                  margin: const EdgeInsets.only(top: 20, left: 0.1, right: 0.1),
                  height: 130,
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black26,
                        blurRadius: 10,
                        offset: Offset(2, 2),
                      )
                    ],
                    borderRadius: BorderRadius.all(Radius.circular(20)),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Container(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text("Attendance of "+selectedDate.toString().substring(0,10).replaceAll(' ', ''),
                          style: TextStyle(
                            fontFamily: "Nexa_light",
                            fontSize: 15,
                            color: Colors.black54,
                          ),),
                      ),

                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "H1",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  if (h1_=='0')
                                    Text(
                                      "A",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: primary,
                                      ),
                                    ),
                                  if (h1_=='1')
                                    Text(
                                      "P",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: Colors.green,
                                      ),
                                    ),

                                ],
                              )),
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "H2",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  if (h2_=='0')
                                    Text(
                                      "A",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: primary,
                                      ),
                                    ),
                                  if (h2_=='1')
                                    Text(
                                      "P",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: Colors.green,
                                      ),
                                    ),


                                ],
                              )),
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "H3",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  if (h3_=='0')
                                    Text(
                                      "A",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: primary,
                                      ),
                                    ),
                                  if (h3_=='1')
                                    Text(
                                      "P",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: Colors.green,
                                      ),
                                    ),


                                ],
                              )),
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "H4",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  if (h4_=='0')
                                    Text(
                                      "A",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: primary,
                                      ),
                                    ),
                                  if (h4_=='1')
                                    Text(
                                      "P",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: Colors.green,
                                      ),
                                    ),


                                ],
                              )),
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "H5",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  if (h5_=='0')
                                    Text(
                                      "A",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: primary,
                                      ),
                                    ),
                                  if (h5_=='1')
                                    Text(
                                      "P",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: Colors.green,
                                      ),
                                    ),


                                ],
                              )),
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "H6",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  if (h6_=='0')
                                    Text(
                                      "A",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: primary,
                                      ),
                                    ),
                                  if (h6_=='1')
                                    Text(
                                      "P",
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontFamily: "Nexa_bold",
                                        color: Colors.green,
                                      ),
                                    ),


                                ],
                              )),
                        ],
                      ),
                    ],
                  ),
                ),
              if (isMonthPicked)
                Container(
                  margin: const EdgeInsets.only(top: 20, left: 0.1, right: 0.1),
                  height: 130,
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black26,
                        blurRadius: 10,
                        offset: Offset(2, 2),
                      )
                    ],
                    borderRadius: BorderRadius.all(Radius.circular(20)),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Container(
                        padding: EdgeInsets.only(bottom: 8),
                        child: Text("Attendance of "+selectedMonth.toString().substring(0,7).replaceAll(' ', ''),
                          style: TextStyle(
                            fontFamily: "Nexa_light",
                            fontSize: 15,
                            color: Colors.black54,
                          ),),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "Total Present",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  Text(
                                    total_,
                                    style: TextStyle(
                                      fontSize: 16,
                                      fontFamily: "Nexa_bold",

                                    ),
                                  ),

                                ],
                              )),
                          Expanded(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  Text(
                                    "Percentage",
                                    style: TextStyle(
                                      fontFamily: "Nexa_light",
                                      fontSize: 20,
                                      color: Colors.black54,
                                    ),
                                  ),
                                  Text(
                                    percentage_+" %",
                                    style: TextStyle(
                                      fontSize: 16,
                                      fontFamily: "Nexa_bold",
                                    ),
                                  ),

                                ],
                              )),


                        ],
                      ),
                    ],

                  ),

                ),
              Container(
                margin: const EdgeInsets.only(top: 20, left: 10, right: 10),
                height: 60,
                decoration: const BoxDecoration(
                  color: Colors.white,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black26,
                      blurRadius: 10,
                      offset: Offset(2, 2),
                    )
                  ],
                  borderRadius: BorderRadius.all(Radius.circular(20)),
                ),
                child: Expanded(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Text(
                          "Attendance till "+mv_.toString(),
                          style: TextStyle(
                            fontFamily: "Nexa_light",
                            fontSize: 20,
                            color: Colors.black54,
                          ),
                        ),
                        Text(
                          ttl_+" %",
                          style: TextStyle(
                            fontSize: 16,
                            fontFamily: "Nexa_bold",

                          ),
                        ),

                      ],
                    )),

              ),
              Container(
                padding: EdgeInsets.only(left: 30, right: 30, top: 20, bottom: 10),
                child: SizedBox(
                  height: 40,
                  child: ElevatedButton(
                    style: ButtonStyle(
                      foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
                      backgroundColor: MaterialStateProperty.all<Color>(primary),
                    ),
                    onPressed: () {
                      Navigator.push(context, MaterialPageRoute(
                        builder: (context) => PSubjectAttendance(title: '',),));
                    },
                    child: Text('Subject-wise Attendance',
                      style: TextStyle(
                          fontFamily: "Nexa_bold",
                          fontSize: 15
                      ),),
                  ),
                ),
              ),



            ],
          ),
        ),
      ),
    );
  }
  void getdata() async {
    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    String lid = sh.getString('lid').toString();
    final urls = Uri.parse('$url/parent_view_attendance/');


    try {
      final data = await http.post(urls, body: {
        'lid': lid,
        'date': selectedDate.toString().substring(0,10).replaceAll(' ', ''),
      });

      if (data.statusCode == 200) {
        var jsonData = json.decode(data.body);

        print(jsonData);
        setState(() {
          h1_ = jsonData['data'][0][1].toString();
          h2_ = jsonData['data'][0][2].toString();
          h3_ = jsonData['data'][0][3].toString();
          h4_ = jsonData['data'][0][4].toString();
          h5_ = jsonData['data'][0][5].toString();
          h6_ = jsonData['data'][0][6].toString();
        });
      } else {
        Fluttertoast.showToast(msg: 'Failed to load data');
      }
    } catch (e) {
      Fluttertoast.showToast(msg: 'Error: $e');
    }
  }



  void getmonthly() async {
    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    String lid = sh.getString('lid').toString();
    final urls = Uri.parse('$url/parent_attendance_month/');

    print(selectedMonth);


    try {
      final data = await http.post(urls, body: {
        'lid': lid,
        'month': selectedMonth.toString().split("-")[1].toString(),
      });
      if (data.statusCode == 200) {
        var jsonData = json.decode(data.body);

        setState(() {
          if (jsonData['data'].length!=0) {
            total_ = jsonData['data'][0]['cnt'].toString();
            percentage_ = jsonData['data'][0]['percentage'].toString();
          }
        });
      } else {
        Fluttertoast.showToast(msg: 'Failed to load data');
      }
    } catch (e) {
      Fluttertoast.showToast(msg: 'Error: $e');
    }
  }



  void gettotal() async {
    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    String lid = sh.getString('lid').toString();
    final urls = Uri.parse('$url/parent_attendance_total/');




    m_=DateTime.now().month.toString();
    print(m_);




    try {
      final data = await http.post(urls, body: {
        'lid': lid,
      });
      if (data.statusCode == 200) {
        var jsonData = json.decode(data.body);

        setState(() {


          if(m_=='1'){
            mv_='January';
          }
          else if(m_=='2'){
            mv_='February';
          }else if(m_=='3'){
            mv_='March';
          }else if(m_=='4'){
            mv_='April';
          }else if(m_=='5'){
            mv_='May';
          }else if(m_=='6'){
            mv_='June';
          }else if(m_=='7'){
            mv_='July';
          }else if(m_=='8'){
            mv_='August';
          }else if(m_=='9'){
            mv_='September';
          }else if(m_=='10'){
            mv_='October';
          }else if(m_=='11'){
            mv_='November';
          }
          else if(m_=='12'){
            mv_='December';
          }



          if (jsonData['data'].length!=0) {
            ttl_ = jsonData['data'][0]['percentage'].toString();
          }
        });
      } else {
        Fluttertoast.showToast(msg: 'Failed to load data');
      }
    } catch (e) {
      Fluttertoast.showToast(msg: 'Error: $e');
    }
  }



}
