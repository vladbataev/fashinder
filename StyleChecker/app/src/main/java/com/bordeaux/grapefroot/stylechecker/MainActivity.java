package com.bordeaux.grapefroot.stylechecker;

import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.media.Image;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.RelativeLayout;

import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;


public class MainActivity extends AppCompatActivity {

    private Camera camera;
    private CameraPreview preview;
    public static final String TAG = "MainActivity";

    public static Camera getCameraInstance() {
        Camera c = null;
        try {
            c = Camera.open();
        } catch (Exception e) {
            Log.d(TAG, e.getMessage(), e);
        }
        return c;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);

        if (ContextCompat.checkSelfPermission(getApplicationContext(),
                android.Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat
                    .requestPermissions(this, new String[]{android.Manifest.permission.CAMERA}, 50);
        }

        ((RelativeLayout)findViewById(R.id.activity_main)).setSystemUiVisibility(View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);

        camera = getCameraInstance();
        Camera.Parameters parameters = camera.getParameters();
        parameters.setFocusMode(Camera.Parameters.FOCUS_MODE_AUTO);
        camera.setParameters(parameters);
        preview = new CameraPreview(this, camera);
        camera.setDisplayOrientation(90);
        FrameLayout previewLayout = (FrameLayout) findViewById(R.id.camera_preview);
        previewLayout.addView(preview);

        findViewById(R.id.button_capture).setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                            camera.takePicture(null, null, new Camera.PictureCallback() {
                                @Override
                                public void onPictureTaken(byte[] data, Camera camera) {
                                    UploadTask uploadTask = new UploadTask();
                                    Bitmap bitmap  = BitmapFactory.decodeByteArray(data, 0, data.length);
                                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                                    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
                                    byte[] compressed = baos.toByteArray();
                                    String imageEncoding = Base64.encodeToString(compressed, Base64.DEFAULT);
                                    uploadTask.execute(imageEncoding);
                                }
                            });
                    }
                }
        );

    }
}