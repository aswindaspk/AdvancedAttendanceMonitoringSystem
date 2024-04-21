import 'dart:convert';

import 'package:ats/home.dart';
import 'package:ats/leaverequest_history.dart';
import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Leave Request Form',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LeaveRequestForm(),
    );
  }
}

class LeaveRequestForm extends StatefulWidget {
  @override
  _LeaveRequestFormState createState() => _LeaveRequestFormState();
}

List<String> list = <String>[];

class _LeaveRequestFormState extends State<LeaveRequestForm> {
  _LeaveRequestFormState() {
    getdata();
  }

  DateTime selectedDate = DateTime.now();
  DateTime selectedDate1 = DateTime.now();
  TextEditingController descriptionController = TextEditingController();
  List<int> staff_id_ = <int>[];
  List<String> staff_name_ = <String>[];
  String dropdownValue1 = "";
  

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate, firstDate: DateTime.now(),
      lastDate: DateTime(2030),

      // 000000,
    );
    if (picked != null && picked != selectedDate)
      setState(() {
        selectedDate = picked;
      });
  }

  Future<void> _selectDate1(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate,
      lastDate: DateTime(2030), firstDate: selectedDate,
      // 000000,
    );
    if (picked != null && picked != selectedDate1)
      setState(() {
        selectedDate1 = picked;
      });
  }

  Color primary = const Color(0xffeef444c);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                alignment: Alignment.centerLeft,
                margin: const EdgeInsets.only(left:20, top: 35, bottom: 8),
                child: Row(
                  children: [
                    Text(
                      "Leave Request",
                      style: TextStyle(fontFamily: "Nexa_bold", fontSize: 30),
                    ),
                    Container(
                      margin: EdgeInsets.only(left: 35),
                      child: IconButton(onPressed: (){
                        Navigator.of(context).push(MaterialPageRoute(builder: (context) => LRHistory(title: '',)));
                      }, icon: Icon(Icons.history),
                      iconSize: 35,),
                    )
                  ],
                ),
              ),
              Container(
                margin: const EdgeInsets.only(top: 12, left: 10, right: 10),
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
                          "Start Date",
                          style: TextStyle(
                            fontFamily: "Nexa_light",
                            fontSize: 20,
                            color: Colors.black54,
                          ),
                        ),
                        TextButton(
                          onPressed: () => _selectDate(context),
                          child: Text(
                            '${selectedDate.day}/${selectedDate.month}/${selectedDate.year}',
                            style: TextStyle(
                              fontSize: 16,
                              fontFamily: "Nexa_bold",
                              color: primary,
                            ),
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
                            "End Date",
                            style: TextStyle(
                              fontFamily: "Nexa_light",
                              fontSize: 20,
                              color: Colors.black54,
                            ),
                          ),
                          TextButton(
                            onPressed: () => _selectDate1(context),
                            child: Text(
                              '${selectedDate1.day}/${selectedDate1.month}/${selectedDate1.year}',
                              style: TextStyle(
                                fontSize: 16,
                                fontFamily: "Nexa_bold",
                                color: primary,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                alignment: Alignment.centerLeft,
                margin: const EdgeInsets.only(top: 40, left: 20),
                child: Text(
                  "Leave Description",
                  style: TextStyle(
                      fontFamily: "Nexa_bold", fontSize: 20),
                ),
              ),
              Container(
                margin: const EdgeInsets.only(left: 10, right: 10),
                // height: 130,

                child: Container(
                  margin: const EdgeInsets.only(top: 4),
                  child: TextFormField(
                    controller: descriptionController,
                    decoration: InputDecoration(
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: BorderSide(
                          color: primary
                        )
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15.0),
                        borderSide: BorderSide(
                          color: Colors.black54
                        )
                      ),
                      // labelText: 'Leave Description',
                      focusColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15.0),
                        borderSide: BorderSide(
                          color: primary
                        )
                      ),
                    ),
                    maxLines: 3,
                  ),
                ),
              ),

              // Container(
              //   decoration: BoxDecoration(
              //     // color: Colors.grey,
              //     border: Border.all(color: Colors.black12),
              //     borderRadius: BorderRadius.circular(8),
              //   ),
              //   child: Row(
              //     mainAxisAlignment: MainAxisAlignment.center,
              //     children: [
              //       Text(
              //         'Select Staff:         ',
              //         style: TextStyle(
              //           fontSize: 15.0,
              //           fontWeight: FontWeight.bold,
              //           color: Colors.black,
              //         ),
              //       ),
              //       DropdownButton<String>(
              //         // isExpanded: true,
              //         value: dropdownValue1,
              //         onChanged: (String? value) {
              //           print(dropdownValue1);
              //           print("Hiiii");
              //           setState(() {
              //             dropdownValue1 = value!;
              //           });
              //         },
              //         items: staff_name_.map((String value) {
              //           return DropdownMenuItem(
              //             value: value,
              //             child: Text(
              //               value,
              //               style: TextStyle(
              //                 fontSize: 15.0,
              //                 fontWeight: FontWeight.bold,
              //                 color: Colors.black,
              //                 // backgroundColor: Colors.brown,
              //               ),
              //             ),
              //           );
              //         }).toList(),
              //       ),
              //     ],
              //   ),
              // ),

              Container(
                alignment: Alignment.centerLeft,
                margin: const EdgeInsets.only(top: 20, left: 20),
                child: Text(
                  "Select Staff",
                  style: TextStyle(
                      fontFamily: "Nexa_bold", fontSize: 20),
                ),
              ),
              Container(
                margin: EdgeInsets.only(top: 4, left: 10, right: 10),
                child: DropdownButtonFormField2<String>(
                  isExpanded: true,
                  decoration: InputDecoration(
                    focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: BorderSide(
                            color: primary
                        )
                    ),
                    // Add Horizontal padding using menuItemStyleData.padding so it matches
                    // the menu padding when button's width is not specified.
                    contentPadding: const EdgeInsets.symmetric(vertical: 16),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(15),
                    ),
                    // Add more decoration..
                  ),
                  hint: const Text(
                    'Send Request To',
                    style: TextStyle(fontSize: 14,
                    fontFamily: "Nexa_light"),
                  ),
                  items:
                      staff_name_.map((item) => DropdownMenuItem<String>(
                    value: item,
                    child: Text(
                      item,
                      style: const TextStyle(
                        fontSize: 14,
                        fontFamily: "Nexa_bold"
                      ),
                    ),
                  ))
                      .toList(),
                  validator: (value) {
                    if (value == null) {
                      return 'Please select a staff.';
                    }
                    return null;
                  },
                  onChanged: (String? value) {
                    print(dropdownValue1);
                    print("Hiiii");
                    setState(() {
                      dropdownValue1 = value!;
                    });
                  },
                  onSaved: (value) {
                    dropdownValue1 = value.toString();
                  },
                  buttonStyleData: const ButtonStyleData(
                    padding: EdgeInsets.only(right: 8),
                  ),
                  iconStyleData: const IconStyleData(
                    icon: Icon(
                      Icons.arrow_drop_down,
                      color: Colors.black45,
                    ),
                    iconSize: 24,
                  ),
                  dropdownStyleData: DropdownStyleData(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(15),
                    ),
                  ),
                  menuItemStyleData: const MenuItemStyleData(
                    padding: EdgeInsets.symmetric(horizontal: 16),
                  ),
                ),
              ),



              Container(
                padding: EdgeInsets.only(left: 10, right: 10, top: 40),
                child: SizedBox(
                  height: 50,
                  child: ElevatedButton(
                    style: ButtonStyle(
                      foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
                      backgroundColor: MaterialStateProperty.all<Color>(primary),
                    ),
                    onPressed: () {
                      sendData();
                      // Submit leave request
                      print('Date: $selectedDate');
                      print('end Date: $selectedDate1');
                      print('Description: ${descriptionController.text}');
                      print(staff_id_[staff_name_.indexOf(dropdownValue1)]
                          .toString());
                    },
                    child: Text('Submit',
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
      ),
    );
  }

  void getdata() async {
    List<int> staff_id = <int>[];
    List<String> staff_name = <String>[];

    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    String lid = sh.getString('lid').toString();
    final urls = Uri.parse('$url/staff_view/');
    // try {
    //   final response = await http.post(urls, body: {
    //     'lid': lid,
    //   });
    var data = await http.post(urls, body: {
      'lid': lid,
    });
    var jsondata = json.decode(data.body);
    String status = jsondata['status'];

    var arr = jsondata["data"];

    for (int i = 0; i < arr.length; i++) {
      staff_id.add(arr[i]['staff_id']);
      staff_name.add(arr[i]['staff_name']);
    }
    setState(() {
      staff_id_ = staff_id;
      staff_name_ = staff_name;
      dropdownValue1 = staff_name_.first;
    });
  }

  void sendData() async {
    String desc_ = descriptionController.text;

    print(staff_name_.indexOf(dropdownValue1));

    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();
    String lid = sh.getString('lid').toString();

    final urls = Uri.parse('$url/leave_request/');
    try {
      final response = await http.post(urls, body: {
        'lid': lid,
        'staffname': staff_id_[staff_name_.indexOf(dropdownValue1)].toString(),
        'sdate': selectedDate.toString(),
        'edate': selectedDate1.toString(),
        'desc': desc_.toString()
      });
      print(jsonDecode(response.body));
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        print(status);
        if (status == 'ok') {
          Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => StudentHome(),
              ));
        } else if (status == "exists") {
          Fluttertoast.showToast(msg: '');
        }
      } else {
        Fluttertoast.showToast(msg: 'Network Error');
      }
    } catch (e) {
      Fluttertoast.showToast(msg: e.toString());
    }
  }

  // catch (e) {
  //   Fluttertoast.showToast(msg: e.toString());
  // }
}
