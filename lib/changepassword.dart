import 'package:ats/home.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:fluttertoast/fluttertoast.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Change Password Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ChangePasswordScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class ChangePasswordScreen extends StatefulWidget {
  @override
  _ChangePasswordScreenState createState() => _ChangePasswordScreenState();
}

class _ChangePasswordScreenState extends State<ChangePasswordScreen> {
  TextEditingController _oldPasswordController = TextEditingController();
  TextEditingController _newPasswordController = TextEditingController();
  TextEditingController _retypePasswordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(
      //   title: Text('Change Password'),
      // ),
      appBar: AppBar(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        automaticallyImplyLeading: false,
        backgroundColor: Color(0xffeef444c),
        elevation: 0,
        leadingWidth: 0.0,
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            CircleAvatar(
              backgroundColor: Colors.transparent,
              radius: 20.0,
              child: IconButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                splashRadius: 1.0,
                icon: Icon(
                  Icons.arrow_back_ios_new,
                  size: 24.0,
                  color: Colors.white,
                ),
              ),
            ),
            Text(
              "Change Password",
              style: TextStyle(fontFamily: "Nexa_bold", color: Colors.white),
            ),
            SizedBox(
              width: 40.0,
            ),
          ],
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _oldPasswordController,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'Old Password',
                labelStyle: TextStyle(
                  fontFamily: "Nexa_light",
                ),
                  focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(
                          color: Color(0xffeef444c)
                      )
                  ),
              ),
            ),
            SizedBox(height: 16.0),
            TextField(
              controller: _newPasswordController,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'New Password',
                  labelStyle: TextStyle(
                    fontFamily: "Nexa_light",
                  ),
                  focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(
                          color: Color(0xffeef444c)
                      )
                  )
              ),
            ),
            SizedBox(height: 16.0),
            TextField(
              controller: _retypePasswordController,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'Retype Password',
                  labelStyle: TextStyle(
                    fontFamily: "Nexa_light",
                  ),
                focusedBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                    color: Color(0xffeef444c)
                  )
                )
              ),
            ),
            SizedBox(height: 32.0),
            ElevatedButton(
              onPressed: () async {

                String old=_oldPasswordController.text;
                String newp=_newPasswordController.text;
                String cpswd=_retypePasswordController.text;
                // Check if new password and retype password match
                if (_newPasswordController.text == _retypePasswordController.text) {
                  // Perform change password operation here
                  SharedPreferences sh = await SharedPreferences.getInstance();
                  String url = sh.getString('url').toString();
                  String lid = sh.getString('lid').toString();
                  // String old =sh.getString('old').toString();
                  // String newp = sh.getString('newp').toString();
                  

                  final urls = Uri.parse('$url/user_change_password/');
                  try {
                    final response = await http.post(urls, body: {
                      'lid':lid,
                      'old':old,
                      'newp':newp,
                      'cp':cpswd,


                    });
                    if (response.statusCode == 200) {
                      String status = jsonDecode(response.body)['status'];
                      if (status=='ok') {

                        _oldPasswordController.clear();
                        _newPasswordController.clear();
                        _retypePasswordController.clear();
                        // Show success message
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Password changed successfully')),
                        );
                        Navigator.push(context, MaterialPageRoute(
                          builder: (context) => StudentHome(),));
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
                  }                  // Clear text fields

                } else {
                  // Show error message if new password and retype password don't match
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('New password and retype password do not match')),
                  );
                }
              },
              child: Text('Change Password',
              style: TextStyle(
                fontFamily: "Nexa_bold",
                fontSize: 20,
                color: Colors.white
              ),),
              style: ButtonStyle(
                backgroundColor: MaterialStateProperty.all<Color>(Color(0xffeef444c)),

              ),
            ),
          ],
        ),
      ),
    );
  }
}
