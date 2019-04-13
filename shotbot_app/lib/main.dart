import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

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

  Color _getColor(name){
    if (_buttons[name]) return Colors.blue;
    else return Colors.black;
  }

  void _onPress(name){
    var result = commandShotbot(name);
    print(result);
    setState(() { 
      _buttons["random"] = false;
      _buttons["edges"] = false;
      _buttons["grounders"] = false;
      _buttons[name] = true;
    });
  }

  Future<http.Response> fetchShotbotState() async {
    final response = await http.get('http://10.0.2.2:5000/api');
    if (response.statusCode == 200) {
      // If server returns an OK response, parse the JSON
      print(response.body);
      return response;
      //return Post.fromJson(json.decode(response.body));
    } else {
      // If that response was not OK, throw an error.
      throw Exception('Failed to load shotbot');
    }
  }

  Future<http.Response> commandShotbot(name) async {
    final response = await http.post('http://10.0.2.2:5000/command?switch='+name);
    if (response.statusCode == 200) {
      // If server returns an OK response, parse the JSON
      print(response.body);
      return response;
      //return Post.fromJson(json.decode(response.body));
    } else {
      // If that response was not OK, throw an error.
      //throw Exception('Failed to command shotbot');
      return response;
    }
  }
  @override
  initState() {
    super.initState();
    fetchShotbotState();
  }

  @override
  Widget build(BuildContext context) {
    Widget buttonSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Icons.blur_on, 'random'),
          _buildButtonColumn(Icons.border_outer, 'edges'),
          _buildButtonColumn(Icons.call_missed_outgoing, 'grounders'),
        ],
      ),
    );

    Widget panPitchSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Icons.code, 'pan'),
          _buildButtonColumn(Icons.exit_to_app, 'pitch'),
        ],
      ),
    );

    Widget upDownSection = Container(
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildButtonColumn(Icons.arrow_upward, 'up'),
          _buildButtonColumn(Icons.arrow_downward, 'down'),
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
              color: Colors.blue,
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
  
  Column _buildButtonColumn(IconData icon, String label) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        IconButton(
              icon: Icon(icon),
              color: _getColor(label),
              tooltip: label,
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
              color: Colors.blue,
            ),
          ),
        ),
      ],
    );
  }
}
