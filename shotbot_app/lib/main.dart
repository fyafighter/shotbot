import 'package:flutter/material.dart';

//RANDOM MODE blur_on → const IconData
//const IconData(58277, fontFamily: 'MaterialIcons')

//Edges: border_outer → const IconData
//const IconData(57903, fontFamily: 'MaterialIcons')

//Grounders: border_bottom → const IconData
//const IconData(57897, fontFamily: 'MaterialIcons')
void main() => runApp(ShotbotApp());

class ShotbotApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shotbot!',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ShotbotPage(title: 'Shotbot!'),
    );
  }

}

class ShotbotPage extends StatefulWidget {
  ShotbotPage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _ShotbotPageState createState() => _ShotbotPageState();
}

class _ShotbotPageState extends State<ShotbotPage> {
  int _counter = 0;
  bool _connected = false;

  var modes = {
    'random': false,
    'edges': false, 
    'grounders': false,
  };
  var relays = {
    'pan': false,
    'pitch': false, 
    'up': false,
    'down': false,
  };

  String _shotbotUrl="http://192.168.86.100/";
  Color color = Colors.blue;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    Widget buttonSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(color, Icons.blur_on, 'Random'),
          _buildButtonColumn(color, Icons.border_outer, 'Edges'),
          _buildButtonColumn(color, Icons.call_missed_outgoing, 'Grounders'),
        ],
      ),
    );

    Widget panPitchSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Colors.black, Icons.code, 'Pan'),
          _buildButtonColumn(Colors.black, Icons.exit_to_app, 'Pitch'),
        ],
      ),
    );

    Widget upDownSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Colors.black, Icons.arrow_upward, 'Up'),
          _buildButtonColumn(Colors.black, Icons.arrow_downward, 'Down'),
        ],
      ),
    );

    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.insert_emoticon),
            tooltip: 'Reconnect',
            onPressed: (){},
          )
        ],
      ),
      body: Column(
        children: <Widget>[
          SizedBox(height: 25),
          Text(
            "Shot Pattern",
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w400,
            ),
          ),
          Text(
            "(shooting will start 10 seconds after pressing)",
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w400,
              color: color,
            ),
          ),
          buttonSection,
          SizedBox(height: 40),
          Text(
            "Controls",
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w400,
            ),
          ),
          panPitchSection,
          SizedBox(height: 30),
          upDownSection,
          SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: RaisedButton(
              onPressed: () {},
              shape: StadiumBorder(),
              child: const Text('Level'),
            ),
          ),
          SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: RaisedButton(
              onPressed: () {},
              shape: StadiumBorder(),
              color: Colors.redAccent,
              textColor: Colors.white,
              child: const Text('Shutdown'),
            ),
          )
        ],
        )
    );
  } // Build
  
  Column _buildButtonColumn(Color color, IconData icon, String label) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
              icon: Icon(icon),
              color: color,
              tooltip: 'label',
              onPressed: () {
              },
            ),
        Container(
          margin: const EdgeInsets.only(top: 8),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w400,
              color: color,
            ),
          ),
        ),
      ],
    );
  }
}
