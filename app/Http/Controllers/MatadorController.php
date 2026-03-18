<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;

class MatadorController extends Controller
{
    public function start()
    {
        $response = Http::get('http://game-engine:81/matador/start');

        return response()->json($response->json());
    }
}