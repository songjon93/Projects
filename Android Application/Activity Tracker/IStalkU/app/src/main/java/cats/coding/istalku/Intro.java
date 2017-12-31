package cats.coding.istalku;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class Intro extends AppCompatActivity {

    private ViewPager mViewPager;
    private MyViewPagerAdapter myViewPagerAdapter;
    private int[] layouts;
    private SharedPreferences sp;

    // A tutorial for the first comers
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_intro);
        sp = PreferenceManager.getDefaultSharedPreferences(this);

        if (!sp.getBoolean("first", true)){
            launch(findViewById(R.id.view_pager));
        }

        mViewPager = (ViewPager) findViewById(R.id.view_pager);

        layouts = new int[]{R.layout.intro_1, R.layout.intro_2, R.layout.intro_3};
        myViewPagerAdapter = new MyViewPagerAdapter();
        mViewPager.setAdapter(myViewPagerAdapter);

    }

    // launch the main activity and mark the tutorial as watched
    public void launch(View view){
        sp.edit().putBoolean("first", false).apply();
        startActivity(new Intent(this, Menu.class));
        finish();
    }

    // A pager adapter for the tutorial slides
    public class MyViewPagerAdapter extends PagerAdapter {
        private LayoutInflater layoutInflater;

        public MyViewPagerAdapter(){
        }

        @Override
        public Object instantiateItem(ViewGroup container, int position) {
            layoutInflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            View view = layoutInflater.inflate(layouts[position], container, false);
            container.addView(view);
            return view;
        }

        @Override
        public int getCount() {
            return layouts.length;
        }

        @Override
        public boolean isViewFromObject(View view, Object object) {
            return view == object;
        }

        @Override
        public void destroyItem(ViewGroup container, int position, Object object) {
            container.removeView((View) object);
        }
    }
}
