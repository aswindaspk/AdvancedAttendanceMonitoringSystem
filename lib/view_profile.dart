

import 'package:ats/changepassword.dart';
import 'package:ats/home.dart';
import 'package:ats/screens/login_screen.dart';
import 'package:flutter/material.dart';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

import 'dart:convert';







void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '',
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      // home:  (title: 'Sent Complaint'),
    );
  }
}


class userProfile_new1 extends StatefulWidget {
  const userProfile_new1({super.key, required this.title});


  final String title;

  @override
  State<userProfile_new1> createState() => _userProfile_new1State();
}
class _userProfile_new1State extends State<userProfile_new1> {
  // @override
  // void initState() {
  //   // TODO: implement initState
  //   super.initState();
  //   senddata();
  // }


  _userProfile_new1State(){
    senddata();
  }





  Color primary = const Color(0xffeef444c);

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async{
        Navigator.push(context, MaterialPageRoute(builder: (context) =>StudentHome(),));

        return false;

      },
      child: Scaffold(
        // backgroundColor: Colors.grey.shade300,
        body:

        SingleChildScrollView(
          child: Stack(
            children: [
              Container(
                padding: EdgeInsets.only(top: 0),
                child: SizedBox(
                  height: 550,
                  width: double.infinity,
                  child: Image.network(
                    photo,
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              // Container(
              //   alignment: Alignment.centerLeft,
              //   margin: const EdgeInsets.only(top: 60, left: 20),
              //   child:
              //   Text(
              //     "$name's Profile",
              //     style: TextStyle(
              //         fontFamily: "Nexa_bold", fontSize: 34),
              //   ),
              // ),
              Container(
                margin: EdgeInsets.only(top: 400, left: 15, right: 15, bottom: 8),
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
                  children: [
                    Stack(
                      children: [
                        Container(
                          padding: EdgeInsets.all(1.0),
                          margin: EdgeInsets.only(top: 16.0),
                          decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(20.0)),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              // Container(
                              //     margin: const EdgeInsets.only(left: 110.0),
                              //     child: Row(
                              //       // mainAxisAlignment: MainAxisAlignment.start,
                              //       crossAxisAlignment: CrossAxisAlignment.start,
                              //       children: [
                              //         Column(
                              //           crossAxisAlignment:
                              //           CrossAxisAlignment.start,
                              //           mainAxisAlignment:
                              //           MainAxisAlignment.start,
                              //           children: [
                              //             Row(
                              //               children: [
                              //                 Text(
                              //                   ' $name',
                              //                   style: Theme.of(context)
                              //                       .textTheme
                              //                       .headline6,
                              //                 ),
                              //                 Container(
                              //                     alignment: Alignment.bottomRight,
                              //                     margin: EdgeInsets.only(left: 72),
                              //                     child:
                              //                     FloatingActionButton(onPressed: (){
                              //                       Navigator.push(context, MaterialPageRoute(builder: (context) => LoginScreen()));
                              //                     },backgroundColor: Colors.white,
                              //                       child: Icon(Icons.logout_rounded),)
                              //                 )
                              //               ],
                              //             ),
                              //             // Text(
                              //             //   'Student',
                              //             //   style: Theme.of(context)
                              //             //       .textTheme
                              //             //       .bodyText1,
                              //             // ),
                              //             SizedBox(
                              //               height: 40,
                              //             )
                              //           ],
                              //         ),
                              //         Spacer(),
                              //         // CircleAvatar(
                              //         //   backgroundColor: Colors.blueAccent,
                              //         //   child: IconButton(
                              //         //       onPressed: () {
                              //         //         // Navigator.push(context, MaterialPageRoute(builder: (context) => editprofile(title: "",),));
                              //         //       },
                              //         //       icon: Icon(
                              //         //         Icons.edit_outlined,
                              //         //         color: Colors.white,
                              //         //         size: 18,
                              //         //       )
                              //         //   ),
                              //         // )
                              //       ],
                              //     )),
                              // SizedBox(height: 10.0),
                              // Row(
                              //   children: [
                              //
                              //   ],
                              // ),
                            ],

                          ),
                        ),
                        // Container(
                        //   height: 90,
                        //   width: 90,
                        //   decoration: BoxDecoration(
                        //       borderRadius: BorderRadius.circular(20.0),
                        //       image:  DecorationImage(
                        //           image: NetworkImage(
                        //               photo),
                        //           fit: BoxFit.cover)),
                        //   margin: EdgeInsets.only(left: 20.0),
                        // ),
                      ],
                    ),
                    const SizedBox(height: 20.0),
                    Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20.0),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children:  [
                          Container(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                Text(
                                  "$name's Profile",
                                  style: TextStyle(
                                      fontFamily: "Nexa_bold", fontSize: 34),
                                ),
                            Container(
                              padding: EdgeInsets.only(left: 10),
                              child: CircleAvatar(
                                          backgroundColor: Colors.blueAccent,
                                          child: IconButton(
                                              onPressed: () {
                                                Navigator.push(context, MaterialPageRoute(builder: (context) => LoginScreen()));
                                              },
                                              icon: Icon(
                                                Icons.logout_rounded,
                                                color: Colors.white,
                                                size: 18,
                                              )
                                          ),
                                        ),
                            )
                              ],
                            ),
                          ),
                          ListTile(
                            title: Text("Name"),
                            subtitle: Text(name),
                            leading: Icon(Icons.person),
                          ),


                          ListTile(
                            title: Text("Gender"),
                            subtitle: Text(gender),
                            leading: Icon(FontAwesomeIcons.venusMars),
                          ),
                          ListTile(
                            title: Text('DOB'),
                            subtitle: Text(dob),
                            leading: Icon(Icons.calendar_today_sharp),
                          ),
                          ListTile(
                            title: Text('Email'),
                            subtitle: Text(email),
                            leading: Icon(Icons.email),
                          ),
                          ListTile(
                            title: Text('Phone'),
                            subtitle: Text(phone),
                            leading: Icon(Icons.phone),
                          ),
                          ListTile(
                            title: Text('House name'),
                            subtitle: Text(house),
                            leading: Icon(Icons.home),
                          ),
                          ListTile(
                            title: Text('Location'),
                            subtitle: Text(location),
                            leading: Icon(FontAwesomeIcons.locationDot),
                          ),
                          ListTile(
                            title: Text('Pin'),
                            subtitle: Text(pin),
                            leading: Icon(FontAwesomeIcons.locationPin),
                          ),
                          ListTile(
                            title: Text('Department'),
                            subtitle: Text(department),
                            leading: Icon(FontAwesomeIcons.print),
                          ),
                          ListTile(
                            title: Text('Course'),
                            subtitle: Text(course),
                            leading: Icon(Icons.post_add_sharp),
                          ),
                          ListTile(
                            title: Text('Sem'),
                            subtitle: Text(sem),
                            leading: Icon(FontAwesomeIcons.paperclip),
                          ),



                        ],
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.only(left: 1, right: 1, top: 10, bottom: 10),
                      child: SizedBox(
                        height: 50,
                        child: ElevatedButton(
                          style: ButtonStyle(
                            foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
                            backgroundColor: MaterialStateProperty.all<Color>(primary),
                          ),
                          onPressed: () {
                            Navigator.push(context, MaterialPageRoute(
                              builder: (context) => ChangePasswordScreen(),));
                          },
                          child: Text('Change Password',
                            style: TextStyle(
                                fontFamily: "Nexa_bold",
                                fontSize: 20
                            ),),
                        ),
                      ),
                    ),


                  ],



                ),
              ),


            ],


          ),


        ),


      ),
    );
  }

  String name='student_name';
  String gender='gender';
  String phone='student_phone';
  String email='student_email';
  String house='student_house';
  String sem = 'sem';
  String location='student_location';
  String pin='student_pincode';
  String photo='student_photo';
  String dob ='student_dob';
  String course ='course';
  String department='department';


  void senddata()async{



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
          String dob_=jsonDecode(response.body)['student_dob'].toString();
          String gender_=jsonDecode(response.body)['gender'].toString();
          String email_=jsonDecode(response.body)['student_email'].toString();
          String phone_=jsonDecode(response.body)['student_phone'].toString();
          String house_=jsonDecode(response.body)['student_house'].toString();
          String location_=jsonDecode(response.body)['student_location'].toString();
          String pin_=jsonDecode(response.body)['student_pincode'].toString();
          String photo_= sh.getString('img_url').toString()+jsonDecode(response.body)['student_photo'].toString();
          String course_=jsonDecode(response.body)['course'].toString();
          String department_=jsonDecode(response.body)['department'].toString();
          String sem_=jsonDecode(response.body)['sem'].toString();


          setState(() {
            name=name_;
            dob=dob_;
            gender=gender_;
            email=email_;
            phone=phone_;
            house=house_;
            location=location_;
            pin=pin_;
            photo=photo_;
            course=course_;
            department=department_;
            sem=sem_;

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