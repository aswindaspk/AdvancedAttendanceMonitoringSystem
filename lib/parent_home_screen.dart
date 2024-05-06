import 'dart:async';
import 'dart:convert';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:intl/intl.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class PHome extends StatefulWidget {
  const PHome({super.key});

  @override
  State<PHome> createState() => _PHomeState();
}

class _PHomeState extends State<PHome> {
  String currentTime = '';
  String currentDay = '';
  String currentDate = '';
  String day = '';
  String uname_ = '';
  String studentname_ = '';
  String time = '';

  _PHomeState() {
    getData();
  }

  double screenHeight = 0;
  double screenWidth = 0;
  Color primary = const Color (0xffeef444c);


  @override


  void initState() {
    super.initState();
    // Update the current time every second
    Timer.periodic(Duration(seconds: 1), (Timer t) => _getCurrentTime());
  }

  void _getCurrentTime() {
    setState(() {
      currentTime = DateFormat.jm().format(DateTime.now());
      currentDay = DateFormat.d().format(DateTime.now());
      currentDate = DateFormat.yMMMM().format(DateTime.now());
      day = DateFormat.EEEE().format(DateTime.now());


    });
  }



  Widget build(BuildContext context) {
    screenHeight = MediaQuery.of(context).size.width;
    screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(top: 50, left: 20),
              child:
              Text(
                "Hi $uname_",
                style: TextStyle(
                    fontFamily: "Nexa_bold", fontSize: screenWidth / 11),
              ),
            ),
            Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(left: 20, bottom: 20),
              child: Text(
                "Welcome back!",
                style: TextStyle(
                    color: Colors.black54,
                    fontFamily: "Nexa_light",
                    fontSize: screenWidth / 15),
              ),
            ),
            Container(
              margin: const EdgeInsets.only(left: 20),
              alignment: Alignment.centerLeft,
              child: Text(
                currentTime,
                style: const TextStyle(
                  fontFamily: "Nexa_bold",
                  fontSize: 20,
                  color: Colors.black54,
                ),
              ),
            ),
            Container(
              margin: const EdgeInsets.only(left: 20),
              alignment: Alignment.centerLeft,
              child: RichText(
                text: TextSpan(
                    text: currentDay+" ",
                    style: TextStyle(
                      fontFamily: "Nexa_bold",
                      fontSize: 25,
                      color: primary,
                    ),
                    children: [
                      TextSpan(
                        text: currentDate,
                        style: const TextStyle(
                          fontFamily: "Nexa_bold",
                          fontSize: 20,
                          color: Colors.black54,
                        ),
                      )
                    ]
                ),
              ),
            ),
            Container(
              margin: const EdgeInsets.only(left: 20),
              alignment: Alignment.centerLeft,
              child: Text(
                day,
                style: const TextStyle(
                  fontFamily: "Nexa_bold",
                  fontSize: 20,
                  color: Colors.black54,
                ),
              ),
            ),
            Container(
              alignment: Alignment.centerLeft,
              margin: const EdgeInsets.only(top: 40, left: 20),
              child: Text(
                "Today's Status",
                style: TextStyle(
                    fontFamily: "Nexa_bold", fontSize: screenWidth / 14),
              ),
            ),
            Container(
              margin: const EdgeInsets.only(top: 12, left: 15, right: 15),
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
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(bottom: 10),
                            child: Text(
                              "$studentname_'s Last Attendance At ",
                              style: TextStyle(
                                fontFamily: "Nexa_light",
                                fontSize: 20,
                                color: Colors.black54,
                              ),
                            ),
                          ),
                          Text(
                            time,
                            style: TextStyle(
                              fontFamily: "Nexa_bold",
                              fontSize: 20,
                            ),
                          ),
                        ],
                      )),
                  // Expanded(
                  //   child: Column(
                  //     mainAxisAlignment: MainAxisAlignment.center,
                  //     crossAxisAlignment: CrossAxisAlignment.center,
                  //     children: [
                  //       Text(
                  //         "Subject",
                  //         style: TextStyle(
                  //           fontFamily: "Nexa_light",
                  //           fontSize: 20,
                  //           color: Colors.black54,
                  //         ),
                  //       ),
                  //       Text(
                  //         "Python",
                  //         style: TextStyle(
                  //           fontFamily: "Nexa_bold",
                  //           fontSize: 20,
                  //         ),
                  //       ),
                  //     ],
                  //   ),
                  // ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }



  void getData()async{



    SharedPreferences sh=await SharedPreferences.getInstance();
    String url=sh.getString('url').toString();
    String lid=sh.getString('lid').toString();
    final urls=Uri.parse(url+"/parent_viewprofile/");
    try{
      final response=await http.post(urls,body:{
        'lid':lid,
      });
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        if (status=='ok') {
          String name_=jsonDecode(response.body)['parent_name'].toString();
          String stname_=jsonDecode(response.body)['student_name'].toString();
          String time_=jsonDecode(response.body)['time'].toString();

          print(name_);
          print(stname_);



          setState(() {
            uname_=name_;
            List<String> name = stname_.split(" ");
            studentname_=name[0];
            time=time_;

            print(studentname_);


          });

        }else {
          Fluttertoast.showToast(msg: 'Not Found');
        }
      }
      else {
        Fluttertoast.showToast(msg: 'Network Error');
      }
    }
    catch (e){
      Fluttertoast.showToast(msg: e.toString());
    }

  }



}
