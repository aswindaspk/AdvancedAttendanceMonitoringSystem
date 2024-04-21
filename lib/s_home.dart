  import 'dart:async';
import 'dart:convert';
  import 'package:ats/screens/login_screen.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:intl/intl.dart';
  import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
  import 'package:http/http.dart' as http;

  class SHome extends StatefulWidget {
    const SHome({super.key});

    @override
    State<SHome> createState() => _SHomeState();
  }

  class _SHomeState extends State<SHome> {
    String currentTime = '';
    String currentDay = '';
    String currentDate = '';
    String day = '';
    String uname_ = '';
    String time = '';
    String subject = '';

    _SHomeState() {
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
                        Text(
                          "Marked At",
                          style: TextStyle(
                            fontFamily: "Nexa_light",
                            fontSize: 20,
                            color: Colors.black54,
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
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            "Subject",
                            style: TextStyle(
                              fontFamily: "Nexa_light",
                              fontSize: 20,
                              color: Colors.black54,
                            ),
                          ),
                          Text(
                            subject,
                            style: TextStyle(
                              fontFamily: "Nexa_bold",
                              fontSize: 20,
                            ),
                          ),
                        ],
                      ),
                    ),
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
      final urls=Uri.parse(url+"/user_viewprofile/");
      try{
        final response=await http.post(urls,body:{
          'lid':lid,
        });
        if (response.statusCode == 200) {
          String status = jsonDecode(response.body)['status'];
          if (status=='ok') {
            String name_=jsonDecode(response.body)['student_name'].toString();
            String time_=jsonDecode(response.body)['time'].toString();
            String subject_=jsonDecode(response.body)['subject'].toString();




            setState(() {
              uname_=name_;
              time=time_;
              subject=subject_;


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
