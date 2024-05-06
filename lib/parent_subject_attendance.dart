
import 'dart:convert';

import 'package:ats/chat.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: PSubjectAttendance(title: 'Subject-wise Attendance'),
    );
  }
}

class PSubjectAttendance extends StatefulWidget {
  const PSubjectAttendance({super.key, required this.title});


  final String title;


  @override
  State<PSubjectAttendance> createState() => _PSubjectAttendanceState();
}

class _PSubjectAttendanceState extends State<PSubjectAttendance> {

  _PSubjectAttendanceState() {
    view_notification();
  }

  List<String> subject_ = <String>[];
  List<String> present_ = <String>[];
  List<String> total_ = <String>[];
  List<String> percentage_ = <String>[];



  Future<void> view_notification() async {
    List<String> subject = <String>[];
    List<String> present = <String>[];
    List<String> total = <String>[];
    List<String> percentage = <String>[];


    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String lid = sh.getString('lid').toString();
      String url = '$urls/parent_attendance_subject/';

      var data = await http.post(Uri.parse(url), body: {
        'lid':lid,

      });
      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {

        subject.add(arr[i]['subject']);
        present.add(arr[i]['present'].toString());
        total.add(arr[i]['total'].toString().toString());
        percentage.add(arr[i]['percentage'].toString());



      }

      setState(() {
        subject_ = subject;
        present_ = present;
        total_ = total;
        percentage_ = percentage;


      });


      print(statuss);
    } catch (e) {
      print("Error ------------------- " + e.toString());
      //there is error during converting file image to base64 encoding.
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            alignment: Alignment.centerLeft,
            margin: const EdgeInsets.only(top: 50, left: 20),
            child:
            Text(
              "Subject-wise Attendance",
              style: TextStyle(
                  fontFamily: "Nexa_bold", fontSize: 34),
            ),
          ),
          Expanded(
            child: ListView.builder(
              physics: BouncingScrollPhysics(),
              itemCount: subject_.length,
              itemBuilder: (BuildContext context, int index) {
                return Container(
                  child: ListTile(
                    onLongPress: () {
                      print("long press" + index.toString());
                    },
                    title: Container(
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
                      // padding: const EdgeInsets.only(),
                      child: Column(
                        children: [ListTile(

                          title: Text(subject_[index],
                            style: TextStyle(
                                fontFamily: "Nexa_bold",
                                fontSize: 14
                            ),
                          ),
                          subtitle: Text(present_[index]+"/"+total_[index],
                            style: TextStyle(
                                fontFamily: "Nexa_light",
                                fontSize: 17
                            ),),
                          trailing: Text(percentage_[index]+" %",
                            style: TextStyle(
                                fontFamily: "Nexa_light",
                                fontSize: 17
                            ),),
                        ),


                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );


  }
}
