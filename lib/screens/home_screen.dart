import 'package:ats/parent_home.dart';
import 'package:flutter/material.dart';
import 'package:ats/components/components.dart';
import 'package:ats/screens/login_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  static String id = 'home_screen';


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(25),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const TopScreenImage(screenImageName: 'img1.png'),
              Expanded(
                child: Padding(
                  padding:
                      const EdgeInsets.only(right: 15.0, left: 15, bottom: 15),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Text(
                          "Hi User",
                      style: TextStyle(
                        fontSize:50,
                        fontFamily: "Nexa_bold",
                      ),),
                      const Text(
                        'Track your attendance seamlessly',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Colors.black54,
                          fontFamily: "Nexa_light",
                          fontSize: 20,
                        ),
                      ),
                      const SizedBox(
                        height: 15,
                      ),
                      Hero(
                        tag: 'login_btn',
                        child: CustomButton(
                          buttonText: 'Get Started',
                          onPressed: () {
                            // Navigator.push(context, MaterialPageRoute(
                            //   builder: (context) => LoginScreen(),));
                            Navigator.push(context, MaterialPageRoute(
                              builder: (context) => LoginScreen(),));
                          },
                        ),
                      ),
                      const SizedBox(
                        height: 25,
                      ),


                    ],
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
