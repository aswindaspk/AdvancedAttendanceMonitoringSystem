
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
      home: const LRHistory(title: 'Flutter Demo Home Page'),
    );
  }
}

class LRHistory extends StatefulWidget {
  const LRHistory({super.key, required this.title});


  final String title;


  @override
  State<LRHistory> createState() => _LRHistoryState();
}

class _LRHistoryState extends State<LRHistory> {

  _LRHistoryState() {
    view_notification();
  }

  List<String> id_ = <String>[];
  List<String> desc_ = <String>[];
  List<String> sdate_ = <String>[];
  List<String> edate_ = <String>[];
  List<String> msg_ = <String>[];



  Future<void> view_notification() async {
    List<String> id = <String>[];
    List<String> desc = <String>[];
    List<String> sdate = <String>[];
    List<String> edate = <String>[];
    List<String> msg = <String>[];


    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String lid = sh.getString('lid').toString();
      String url = '$urls/leave_history/';
      print(id);
      var data = await http.post(Uri.parse(url), body: {
        'lid':lid,

      });
      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {
        id.add(arr[i]['id'].toString());
        desc.add(arr[i]['desc']);
        sdate.add(arr[i]['sdate'].toString());
        edate.add(arr[i]['edate'].toString());
        msg.add(arr[i]['msg']);



      }

      setState(() {
        id_ = id;
        desc_ = desc;
        sdate_ = sdate;
        edate_ = edate;
        msg_ = msg;

      });

      print(msg_);

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
              "Leave Request History",
              style: TextStyle(
                  fontFamily: "Nexa_bold", fontSize: 34),
            ),
          ),
          Expanded(
            child: ListView.builder(
              physics: BouncingScrollPhysics(),
              itemCount: id_.length,
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

                          title: Text(sdate_[index]+" to "+edate_[index],
                            style: TextStyle(
                              fontFamily: "Nexa_bold",
                              fontSize: 14
                            ),
                          ),
                          subtitle: Text(desc_[index],
                            style: TextStyle(
                              fontFamily: "Nexa_light",
                              fontSize: 17
                            ),),
                          trailing: () {
                            if (msg_[index] == 'Approved') {
                              return Icon(CupertinoIcons.checkmark_alt_circle, color: Colors.green);
                            } else if (msg_[index] == 'Rejected') {
                              return Icon(CupertinoIcons.xmark_circle, color: Colors.red);
                            } else if (msg_[index]=='Pending'){
                              return Icon(CupertinoIcons.hourglass, color: Colors.blue);
                            }
                          }(),
                          onTap: () async {

                          },
                          onLongPress: () {
                            // Handle onLongPress action here
                          },
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
