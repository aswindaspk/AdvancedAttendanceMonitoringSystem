
import 'package:ats/changepassword.dart';
import 'package:ats/daaate.dart';
import 'package:ats/home.dart';
import 'package:ats/leave_request.dart';
import 'package:ats/login.dart';
import 'package:ats/parent_home.dart';
import 'package:ats/screens/home_screen.dart';
import 'package:ats/screens/login_screen.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';


import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import 'main.dart';


void main() {
  runApp(const MyLogin());
}

class MyLogin extends StatelessWidget {
  const MyLogin({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IP Page',
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const IPpage(title: 'IP Page'),
    );
  }
}

class IPpage extends StatefulWidget {
  const IPpage({super.key, required this.title});

  final String title;

  @override
  State<IPpage> createState() => _IPpageState();
}

class _IPpageState extends State<IPpage> {



  TextEditingController ipController = new TextEditingController();


  @override
  Widget build(BuildContext context) {

    return WillPopScope(
      onWillPop: () async{ return true; },
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: Text(widget.title),
        ),


        body: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[

              Padding(
                padding: const EdgeInsets.all(8),
                child: TextField(
                  controller: ipController,
                  decoration: InputDecoration(border: OutlineInputBorder(),label: Text("IP")),
                ),
              ),

              ElevatedButton(
                onPressed: () {

    _send_data();




    },
                child: Text("Connect"),
              ),

            ],
          ),
        ),
      ),
    );
  }


  void _send_data() async{


    String ip=ipController.text;



    SharedPreferences sh = await SharedPreferences.getInstance();
          sh.setString("url", "http://$ip:8000/myapp");
          sh.setString("img_url", "http://$ip:8000");

          Navigator.push(context, MaterialPageRoute(
            builder: (context) => HomeScreen(),));
            // builder: (context) => ParentHome(),));
            // builder: (context) => StudentHome(),));
            // builder: (context) => ChangePasswordScreen(),));


  }

}
