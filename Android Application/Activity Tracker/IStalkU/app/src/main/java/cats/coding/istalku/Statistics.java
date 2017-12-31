package cats.coding.istalku;

import android.content.Context;
import android.graphics.Color;
import android.graphics.DashPathEffect;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.github.mikephil.charting.charts.*;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.data.Entry;
import com.google.android.gms.maps.model.LatLng;

import java.text.DecimalFormat;
import java.text.FieldPosition;
import java.text.Format;
import java.text.ParsePosition;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class Statistics extends Fragment {
    Menu curActivity;
    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_statistics, container, false);
        BarChart barChart = view.findViewById(R.id.chart);
        TextView dist = view.findViewById(R.id.distance_traveled);
        TextView steps = view.findViewById(R.id.steps_taken);
        TextView max_speed = view.findViewById(R.id.max_speed);
        curActivity = (Menu) getActivity();

        // update the view
        drawGraph(barChart);
        DecimalFormat decimalFormat = new DecimalFormat("#.##");
        dist.setText(decimalFormat.format(curActivity.totalDist) + " km");
        max_speed.setText(decimalFormat.format(curActivity.max_speed) + " km / h");
        steps.setText(String.valueOf(curActivity.mSteps) + " steps");
        return view;
    }

    // get an hourly data to display on graph
    public Float[] getData(){
        Float[] data = new Float[24];
        if (curActivity.dataList != null){
            int i = 0;
            for (HourlyData datum : curActivity.hourlyDataList){
                if(datum == null) data[i] = 0f;
                else data[i] = Float.valueOf(datum.getDistance());
                i++;
            }
        }
        return data;
    }

    // drawGraph with the accumulated data
    public void drawGraph(BarChart barChart){
        Float[] data = getData();
        List<BarEntry> entries = new ArrayList<>();

        float i = 0;
        for (Float datum : data){
            if (datum == null) entries.add(new BarEntry(i, 0f));
            else entries.add(new BarEntry(i, datum));
            i += 1;
        }

        BarDataSet dataSet = new BarDataSet(entries, "");
        dataSet.setColor(Color.BLACK);
        dataSet.setValueTextColor(Color.TRANSPARENT);

        BarData barData = new BarData(dataSet);
        barChart.setData(barData);
        barChart.getLegend().setEnabled(false);
        barChart.setFitBars(true);
        barChart.setDrawGridBackground(false);
        barChart.setDescription(null);
        barChart.setBackgroundColor(Color.WHITE);
        barChart.setNoDataText("No Tracked Activity");
        barChart.setDrawBorders(true);

        YAxis y = barChart.getAxisLeft();
        barChart.getAxisRight().setEnabled(false);
        y.setAxisMinimum(0);
        y.setDrawLabels(true);
        XAxis x = barChart.getXAxis();
        x.setAxisMinimum(0);
        x.setPosition(XAxis.XAxisPosition.BOTTOM);
        x.setLabelCount(24);
        x.setDrawLabels(true);
        x.setAxisMaximum(24);
        barChart.invalidate();
    }

    @Override
    public void onResume() {
        super.onResume();
    }

    @Override
    public void onPause() {
        super.onPause();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
    }

    // Source: https://rosettacode.org/wiki/Haversine_formula#Java
    public static class Haversine {
        public static final double R = 6372.8; // In kilometers
        public static double haversine(double lat1, double lon1, double lat2, double lon2) {
            double dLat = Math.toRadians(lat2 - lat1);
            double dLon = Math.toRadians(lon2 - lon1);
            lat1 = Math.toRadians(lat1);
            lat2 = Math.toRadians(lat2);

            double a = Math.pow(Math.sin(dLat / 2),2) + Math.pow(Math.sin(dLon / 2),2) * Math.cos(lat1) * Math.cos(lat2);
            double c = 2 * Math.asin(Math.sqrt(a));
            return R * c;
        }
        public static void main(String[] args) {
            System.out.println(haversine(36.12, -86.67, 33.94, -118.40));
        }
    }
}
