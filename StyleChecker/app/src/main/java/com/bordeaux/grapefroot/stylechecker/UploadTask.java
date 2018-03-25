package com.bordeaux.grapefroot.stylechecker;

import android.media.Image;
import android.os.AsyncTask;

import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class UploadTask extends AsyncTask<String, Integer, Integer> {
    @Override
    protected Integer doInBackground(String... params) {
        URL url = null;
        try {
            url = new URL("fixme");
        } catch (MalformedURLException e) {
            e.printStackTrace();
            return 0;
        }
        try {
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setChunkedStreamingMode(0);
            urlConnection.setDoOutput(true);

            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            out.write(params[0].getBytes());
            return 1;
        } catch (IOException e) {
            e.printStackTrace();
            return 0;
        }
    }
}
