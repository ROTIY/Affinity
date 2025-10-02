import 'dart:convert';
import 'package:http/http.dart' as http;

class MusicService {
  static const String baseUrl = 'http://127.0.0.1:8000'; // Change to your backend URL

  Future<List<Map<String, dynamic>>> fetchSongs() async {
    final response = await http.get(Uri.parse('$baseUrl/songs'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.cast<Map<String, dynamic>>();
    } else {
      throw Exception('Failed to load songs');
    }
  }
}
