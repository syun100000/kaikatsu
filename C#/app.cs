using System;
using System.Windows.Forms;

namespace KikatsuClubFeeCalculator
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void calculateButton_Click(object sender, EventArgs e)
        {
            int age = (int)ageNumericUpDown.Value;
            int duration = (int)durationNumericUpDown.Value;
            string checkinTime = checkinTimeDateTimePicker.Value.ToString("HH:mm");
            int first30MinFee = (int)first30MinFeeNumericUpDown.Value;
            int every10MinFee = (int)every10MinFeeNumericUpDown.Value;
            int[] packFees = {
                (int)pack3hrFeeNumericUpDown.Value,
                (int)pack6hrFeeNumericUpDown.Value,
                (int)pack9hrFeeNumericUpDown.Value,
                (int)pack12hrFeeNumericUpDown.Value,
                (int)pack15hrFeeNumericUpDown.Value,
                (int)pack18hrFeeNumericUpDown.Value,
                (int)pack21hrFeeNumericUpDown.Value,
                (int)pack24hrFeeNumericUpDown.Value
            };
            int night8HrFee = (int)night8hrFeeNumericUpDown.Value;
            bool studentDiscount = studentDiscountCheckBox.Checked;

            int fee = 0;

            if (age <= 12)
            {
                fee = 0;
            }
            else
            {
                int checkinHour = int.Parse(checkinTime.Split(':')[0]);
                bool nightPackAvailable = checkinHour >= 20 || checkinHour < 4;

                int packIndex = duration / 180;
                if (packIndex > 7) packIndex = 7;

                int packFee = packFees[packIndex];

                if (age >= 65)
                {
                    packFee = (int)(packFee * 0.9);
                }
                else if (studentDiscount)
                {
                    packFee = (int)(packFee * 0.8);
                }

                int regularFee = first30MinFee;
                int remainingDuration = duration - 30;
                while (remainingDuration > 0)
                {
                    regularFee += every10MinFee;
                    remainingDuration -= 10;
                }

                fee = Math.Min(packFee, regularFee);

                if (nightPackAvailable && duration <= 480)
                {
                    fee = Math.Min(fee, night8HrFee);
                }
            }

            feeLabel.Text = fee.ToString() + "円";
            resultGroupBox.Visible = true;
        }
    }
}