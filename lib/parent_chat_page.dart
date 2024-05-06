
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
      home: const ViewStaff(title: 'Flutter Demo Home Page'),
    );
  }
}

class ViewStaff extends StatefulWidget {
  const ViewStaff({super.key, required this.title});


  final String title;


  @override
  State<ViewStaff> createState() => _ViewStaffState();
}

class _ViewStaffState extends State<ViewStaff> {

  _ViewStaffState() {
    view_notification();
  }

  List<String> id_ = <String>[];
  List<String> name_ = <String>[];
  List<String> photo_ = <String>[];



  Future<void> view_notification() async {
    List<String> id = <String>[];
    List<String> name = <String>[];
    List<String> photo = <String>[];


    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String lid = sh.getString('lid').toString();
      String url = '$urls/view_staff_chat/';
print(id);
      var data = await http.post(Uri.parse(url), body: {
     'lid':lid,

      });
      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {
        id.add(arr[i]['staff_id'].toString());
        name.add(arr[i]['staff_name']);
        photo.add(sh.getString('img_url').toString()+ arr[i]['staff_photo']);

      }

      setState(() {
        id_ = id;
        name_ = name;
        photo_ = photo;

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
              "Chats",
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
                      leading: CircleAvatar(
                      backgroundImage: NetworkImage(photo_[index]),
                    ),
                    title: Text(
                      name_[index],
                      style: TextStyle(
                        fontFamily: "Nexa_bold",
                      ),
                    ),
                    subtitle: Text("Press to open chat",
                    style: TextStyle(
                      fontFamily: "Nexa_light",
                    ),),
                    onTap: () async {
                      SharedPreferences sh = await SharedPreferences.getInstance();
                      sh.setString("aid", id_[index]).toString();
                      sh.setString("agrname", name_[index]);

                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => MyChatPage(title: '',)),
                      );
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
