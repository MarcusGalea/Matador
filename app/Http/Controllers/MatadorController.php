<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;

class MatadorController extends Controller
{
    public function start()
    {
        $response = Http::get('http://game-engine:81/matador/example_game_start');

        return response()->json([
            'status' => $response->status(),
            'headers' => $response->headers(),
            'body' => $response->body(),
            'json' => $response->json(),
            'successful' => $response->successful(),
        ]);
        // return response()->json($response->json());
    }
}