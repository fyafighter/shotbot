import 'package:flutter/material.dart';
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


  var _buttons = {
    'random': false,
    'edges': false, 
    'grounders': false,
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

  Color _getColor(name){
    if (_buttons[name]) return Colors.blue;
    else return Colors.black;
  }

  void _onPress(name){
    setState(() { 
      if (_buttons[name]) _buttons[name] = false;
      else _buttons[name] = true;
    });
  }

  @override
  initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    Widget buttonSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(color, Icons.blur_on, 'random'),
          _buildButtonColumn(color, Icons.border_outer, 'edges'),
          _buildButtonColumn(color, Icons.call_missed_outgoing, 'grounders'),
        ],
      ),
    );

    Widget panPitchSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Colors.black, Icons.code, 'pan'),
          _buildButtonColumn(Colors.black, Icons.exit_to_app, 'pitch'),
        ],
      ),
    );

    Widget upDownSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Colors.black, Icons.arrow_upward, 'up'),
          _buildButtonColumn(Colors.black, Icons.arrow_downward, 'down'),
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
              color: _getColor(label),
              tooltip: 'label',
              onPressed: () {
                _onPress(label);
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
