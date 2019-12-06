# Generated by Django 2.2.1 on 2019-05-05 11:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher', models.CharField(max_length=500)),
                ('pub_type', models.CharField(choices=[('N', 'News'), ('HB', 'History and Biography'), ('B', 'Bible Study'), ('O', 'Others')], max_length=100)),
                ('title', models.CharField(max_length=1000)),
                ('content', models.TextField()),
                ('pub_date_et_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('article_image', models.ImageField(upload_to='home/articles')),
            ],
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=1000)),
                ('filetype', models.CharField(choices=[('M', 'Music'), ('V', 'Video'), ('Pic', 'Pictures'), ('Pdf', 'Pdf'), ('O', 'Others')], max_length=100)),
                ('upload_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_name', models.CharField(max_length=500, unique=True)),
                ('forum_logo', models.ImageField(upload_to='forum logos')),
                ('forum_type', models.CharField(choices=[('PUBLIC', 'public'), ('PRIVATE', 'private')], max_length=15)),
                ('forum_description', models.TextField(default='This forum was created to....')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(default='UNKNOWN', max_length=50)),
                ('lastname', models.CharField(default='UNKNOWN', max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=14)),
                ('D_O_B', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=50)),
                ('passwd', models.CharField(max_length=64)),
                ('function_held', models.CharField(max_length=30)),
                ('pix', models.ImageField(upload_to='home/images/members_image')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_by', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('source_forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Forum')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Anonymous', max_length=50)),
                ('reply', models.TextField()),
                ('reply_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_name', models.CharField(max_length=100, unique=True)),
                ('content_store', models.TextField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Page')),
            ],
        ),
        migrations.CreateModel(
            name='MessageReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_by', models.CharField(max_length=50)),
                ('reply_to', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('source_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Message')),
            ],
        ),
        migrations.CreateModel(
            name='ForumDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('total_no_of_members', models.CharField(max_length=10)),
                ('source_forum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Forum')),
            ],
        ),
        migrations.AddField(
            model_name='forum',
            name='forum_members',
            field=models.ManyToManyField(to='home.Member'),
        ),
        migrations.CreateModel(
            name='DownloadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster', models.ImageField(upload_to='downloads/posters')),
                ('data', models.FileField(upload_to='downloads')),
                ('download', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Download')),
            ],
        ),
    ]