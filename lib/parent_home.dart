

import 'package:ats/attendance.dart';
import 'package:ats/chat.dart';
import 'package:ats/leave_request.dart';
import 'package:ats/parent_attendance.dart';
import 'package:ats/parent_chat_page.dart';
import 'package:ats/parent_home_screen.dart';
import 'package:ats/parent_profile.dart';
import 'package:ats/s_home.dart';
import 'package:ats/view_attendance.dart';
import 'package:ats/view_profile.dart';
import 'package:flutter/material.dart';
import 'package:flutter_keyboard_visibility/flutter_keyboard_visibility.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class ParentHome extends StatefulWidget {
  const ParentHome({super.key});

  @override
  State<ParentHome> createState() => _ParentHomeState();
}

class _ParentHomeState extends State<ParentHome> {
  double screenHeight = 0;
  double screenWidth = 0;
  Color primary = const Color (0xffeef444c);

  int currentIndex = 0;

  List<IconData> navigationIcons = [
    FontAwesomeIcons.house,
    FontAwesomeIcons.message,
    FontAwesomeIcons.check,
    FontAwesomeIcons.user,
  ];


  @override
  Widget build(BuildContext context) {

    // final bool isKeyboardVisible =KeyboardVisibilityProvider.isKeyboardVisible(context);
    screenHeight=MediaQuery.of(context).size.width;
    screenWidth=MediaQuery.of(context).size.width;


    return Scaffold(
      body: IndexedStack(
        index: currentIndex,
        children: [
          PHome(),
          ViewStaff(title: '',),
          PAttendanceNew(),
          ParentProfile(title: '',),

        ],
      ),
      bottomNavigationBar: Container(
        height: 65,
        margin: const EdgeInsets.only(
          left: 12,
          right: 12,
          bottom: 15,
        ),
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.all(Radius.circular(40)),
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 10,
              offset: Offset(2, 2),
            )
          ],
        ),
        child: ClipRRect(
          borderRadius: const BorderRadius.all(Radius.circular(40)),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              for(int i = 0; i < navigationIcons.length; i++)...<Expanded>{
                Expanded(child: GestureDetector(
                  onTap: () {
                    setState(() {
                      currentIndex = i;
                    });
                  },
                  child: Container(
                    height: screenHeight,
                    width: screenWidth,
                    color: Colors.white,
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            navigationIcons[i],
                            color: i == currentIndex ? primary : Colors.black54,
                            size: i == currentIndex ? 26 : 24,
                          ),
                          i == currentIndex ? Container(
                            margin: EdgeInsets.only(top: 6),
                            height: 3,
                            width: 22,
                            decoration: BoxDecoration(
                                borderRadius: const BorderRadius.all(Radius.circular(40)),
                                color: primary
                            ),
                          ) : const SizedBox(),
                        ],
                      ),
                    ),
                  ),
                ))
              }
            ],
          ),
        ),
      ),
    );
  }

}
