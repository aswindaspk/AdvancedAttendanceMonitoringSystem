import 'package:ats/home.dart';
import 'package:ats/parent_home.dart';
import 'package:flutter/material.dart';
import 'package:ats/components/components.dart';
import 'package:ats/constants.dart';
import 'package:ats/screens/welcome.dart';
import 'package:loading_overlay/loading_overlay.dart';
import 'package:ats/screens/home_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';

import 'dart:convert';

import 'package:slide_to_act/slide_to_act.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  static String id = 'login_screen';

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  TextEditingController unameController = new TextEditingController();
  TextEditingController passController = new TextEditingController();
  bool _obscurePassword = true;
  late String _email;
  late String _password;
  bool _saving = false;
  Color primary = const Color(0xffeef444c);

  @override


  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        Navigator.push(context, MaterialPageRoute(builder: (context) =>HomeScreen(),));
        return false;
      },
      child: Scaffold(
        backgroundColor: Colors.white,
        body: LoadingOverlay(
          isLoading: _saving,
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  const TopScreenImage(screenImageName: 'img2.jpg'),
                  Expanded(
                    flex: 2,
                    child: SingleChildScrollView(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Container(
                            padding: EdgeInsets.only(top: 30, bottom: 20),
                            child: Text(
                              "Welcome back!",
                              style:
                                  TextStyle(fontFamily: "Nexa_bold", fontSize: 35),
                            ),
                          ),
                          CustomTextField(
                            textField: TextField(
                                // controller: unameController,
                                onChanged: (value) {
                                  _email = value;
                                },
                                style: const TextStyle(
                                    fontSize: 20, fontFamily: "Nexa_light"),
                                decoration: kTextInputDecoration.copyWith(
                                    hintText: 'Email')),
                          ),
                          Container(
                            padding: EdgeInsets.only(top: 30, bottom: 50),
                            child: CustomTextField(
                              textField: TextField(
                                // controller: passController,
                                // obscureText: true,
                                obscureText: _obscurePassword,
                                onChanged: (value) {
                                  _password = value;
                                },
                                style: const TextStyle(
                                    fontSize: 20, fontFamily: "Nexa_light"),
                                decoration: kTextInputDecoration.copyWith(
                                    hintText: 'Password',
                                  suffixIcon: Padding(
                                    padding: const EdgeInsets.only(left: 10),
                                    child: IconButton(
                                      icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off),
                                      onPressed: () {
                                        setState(() {
                                          _obscurePassword = !_obscurePassword; // Toggle password visibility
                                        });
                                      },
                                    ),
                                  ),),
                              ),
                            ),
                          ),
                          // CustomBottomScreen(
                          //   textButton: 'Login',
                          //   heroTag: 'login_btn',
                          //   question: 'Forgot password?',
                          //   buttonPressed: () async {
                          //     _send_data();
                          //   },
                          //   questionPressed: () {
                          //     signUpAlert(
                          //       onPressed: () async {
                          //       },
                          //       title: 'RESET YOUR PASSWORD?',
                          //       desc:
                          //           'Click on the button to reset your password',
                          //       btnText: 'Reset Now',
                          //       context: context,
                          //
                          //     ).show();
                          //   },
                          //
                          // ),
                          Column(
                            children: [
                              GestureDetector(
                                onTap: () {
                                  _send_data();
                                },
                                child: Container(
                                  alignment: Alignment.center,
                                  height: 50,
                                  width: 170,
                                  decoration: BoxDecoration(
                                    color: primary,
                                    borderRadius: BorderRadius.circular(60),
                                  ),
                                  child: Text(
                                    "Log In",
                                    style: TextStyle(
                                        color: Colors.white,
                                        fontSize: 20,
                                        fontFamily: "Nexa_bold"),
                                  ),
                                ),
                              ),
                              TextButton(
                                onPressed: () {
                                  // resetpassword();
                                  showDialog(
                                    context: context,
                                    builder: (BuildContext context) {
                                      return ChangePasswordDialog(title: _email,);
                                    },
                                  );
                                },
                                child: Text(
                                  'Forgot Password?',
                                  style: TextStyle(
                                      color: Colors.black54,
                                      fontFamily: "Nexa_bold"),
                                ),
                              ),
                            ],
                          )
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _send_data() async {

    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    sh.setString("email", _email).toString();

    final urls = Uri.parse('$url/user_loginpost/');
    try {
      final response = await http.post(urls, body: {
        'username': _email,
        'password': _password,
      });
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        if (status == 'ok') {
          String type = jsonDecode(response.body)['type'];
          if (type == 'student') {
            String lid = jsonDecode(response.body)['lid'];
            sh.setString("lid", lid);

            Navigator.push(
                context as BuildContext,
                MaterialPageRoute(
                  builder: (context) => StudentHome(),
                ));
          } else if (type == 'parent') {
            String lid = jsonDecode(response.body)['lid'];
            sh.setString("lid", lid);

            Navigator.push(
                context as BuildContext,
                MaterialPageRoute(
                  builder: (context) => ParentHome(),
                ));
          }
        } else {
          Fluttertoast.showToast(msg: 'Incorrect Username or Password');
        }
      } else {
        Fluttertoast.showToast(msg: 'Network Error');
      }
    } catch (e) {
      Fluttertoast.showToast(msg: e.toString());
    }
  }



  // void resetpassword() async{
  //   SharedPreferences sh = await SharedPreferences.getInstance();
  //   String url = sh.getString('url').toString();
  //   String em = sh.getString('email').toString();
  //   final urls = Uri.parse('$url/forget_password/');
  //   final response = await http.post(urls, body: {
  //     'username': em,
  //   });
  //
  //
  //   // Navigator.push(
  //   //     context as BuildContext,
  //   //     MaterialPageRoute(
  //   //       builder: (context) => LoginScreen(),
  //   //     ));
  //
  //
  // }




}






class ChangePasswordDialog extends StatelessWidget {
  ChangePasswordDialog({super.key, this.title});
  final String? title;

  Color primary = const Color(0xffeef444c);
  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(40.0),
      ),
      child: Container(
        color: Colors.transparent,
        height: 120,
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Builder(builder: (context) {
                final GlobalKey<SlideActionState> key = GlobalKey();
                return SlideAction(
                  outerColor: Colors.white,
                  innerColor: primary,
                  key: key,
                  onSubmit: (){
                    resetpassword(title.toString());
                    key.currentState!.reset();
                  },
                  child: Container(
                    margin: EdgeInsets.only(left: 25,top: 6),
                    child: Text(
                      "Slide to reset",
                      style: TextStyle(
                        fontFamily: "Nexa_bold",
                        color: primary,
                        fontSize: 20,
                      ),
                    ),
                  ),
                );
              },
              ),
            ],
          ),
        ),
      ),
    );
  }


  void resetpassword(email) async{
    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    String em = sh.getString('email').toString();
    final urls = Uri.parse('$url/forget_password/');
    final response = await http.post(urls, body: {
      'username': email,
    });


    // Navigator.push(
    //     context as BuildContext,
    //     MaterialPageRoute(
    //       builder: (context) => LoginScreen(),
    //     ));


  }

}
